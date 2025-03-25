import asyncio
import uuid
import os
from typing import Dict, List, Optional, Union, Set, Tuple
from zmp_manual_backend.models.manual import (
    Manual,
    Folder,
    PublishStatus,
    SolutionType,
    JobState,
    FailureReason,
    Notification,
    NotificationType,
)
from zmp_notion_exporter import NotionPageExporter
from zmp_notion_exporter.utility import transform_block_id_to_uuidv4, validate_page_id

# from zmp_notion_exporter.node import Node
from zmp_md_translator import MarkdownTranslator
import git
from dotenv import load_dotenv
import logging
from notion_client import AsyncClient
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Load environment variables
load_dotenv()

logger = logging.getLogger("appLogger")


class ManualService:
    def __init__(
        self,
        notion_token: str,
        root_page_id: str,
        repo_path: str = "./repo",
        source_dir: str = "docs",
        target_dir: str = "i18n",
        github_repo_url: Optional[str] = None,
        target_languages: Optional[Set[str]] = None,
    ):
        """Initialize ManualService.

        Args:
            notion_token: Notion API token
            root_page_id: ID of the root Notion page for ZCP docs
            repo_path: Path to the local repository
            source_dir: Source directory for documentation in the repo
            target_dir: Target directory for translations in the repo
            github_repo_url: URL of the GitHub repository for pushing changes
            target_languages: Set of target languages for translation
        """
        self.notion_token = notion_token
        self.repo_path = Path(repo_path).absolute()
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.github_repo_url = github_repo_url
        self.target_languages = (
            target_languages if target_languages is not None else {"ko", "ja", "zh"}
        )

        # This map holds solutions and their respective root IDs
        self.root_page_ids = {}

        # First try to get solution-specific root page IDs from environment variables
        for solution_type in SolutionType:
            env_var_name = f"{solution_type.value.upper()}_ROOT_PAGE_ID"
            page_id = os.environ.get(env_var_name)
            if page_id:
                self.root_page_ids[solution_type] = page_id
                logger.info(f"Using {env_var_name}: {page_id[:8]}...")

        # For backward compatibility, also check the root_page_id parameter
        if root_page_id and "-" in root_page_id:
            # Format:  zcp:xxxxxx,apim:yyyyyyy,amdp:zzzzz
            for solution_mapping in root_page_id.split(","):
                if ":" in solution_mapping:
                    solution_type, page_id = solution_mapping.split(":", 1)
                    try:
                        solution_enum = SolutionType(solution_type.lower())
                        # Only set if not already set from environment variables
                        if solution_enum not in self.root_page_ids:
                            self.root_page_ids[solution_enum] = page_id
                            logger.info(
                                f"Using {solution_type} from root_page_id parameter: {page_id[:8]}..."
                            )
                    except ValueError as e:
                        logger.warning(
                            f"Invalid solution type in root_page_id: {solution_type}. Error: {str(e)}"
                        )
        elif root_page_id:  # If no mapping, assume it's just the ZCP root ID
            # Only set if not already set from environment variables
            if SolutionType.ZCP not in self.root_page_ids:
                self.root_page_ids[SolutionType.ZCP] = root_page_id
                logger.info(
                    f"Using ZCP root page ID from parameter: {root_page_id[:8]}..."
                )

        if not self.root_page_ids:
            logger.warning("No root page IDs provided for any solution")

        # Notification system
        self.notifications: List[Notification] = []
        self.notification_clients: Dict[str, Tuple[asyncio.Queue, Optional[str]]] = {}

        # Job tracking
        self.active_jobs: Dict[str, PublishStatus] = {}
        self.executor = ThreadPoolExecutor(max_workers=3)

        logger.info(
            f"ManualService initialized with root page IDs: {self.root_page_ids}"
        )

        # Initialize Notion client
        self.notion = AsyncClient(auth=notion_token)

    def _create_translation_progress_callback(self, job_id: str):
        """Create a progress callback for the translation process for a specific job."""

        async def translation_progress_callback(progress):
            """Update translation progress for a specific job."""
            if job_id in self.active_jobs:
                job = self.active_jobs[job_id]

                if progress.status.value == "preparing":
                    job.translation_progress = 0
                    logger.info(job.message)
                elif progress.status.value == "translating":
                    if progress.total > 0:
                        # Calculate progress percentage for translation
                        progress_percentage = round(
                            (progress.current / progress.total) * 100, 1
                        )
                        job.translation_progress = progress_percentage

                    # Initialize file_path with a default value
                    file_path = ""

                    # Extract the relevant part of the file path to make it more readable
                    if progress.current_file:
                        file_path = progress.current_file

                        # Remove job directory and repository path information
                        # Get only the relevant document path
                        if "/current/" in file_path:
                            file_path = file_path.split("/current/", 1)[1]
                        # If we still have a long path with repo details, try other approaches
                        elif "/repo/" in file_path and "/i18n/" in file_path:
                            file_path = file_path.split("/i18n/", 1)[1]
                            parts = file_path.split("/")
                            if len(parts) > 3:  # Language/plugin/current/file.md
                                file_path = "/".join(
                                    parts[3:]
                                )  # Get just the file path

                        # Special case for empty or unclear paths
                        if not file_path or file_path.startswith("/"):
                            file_path = os.path.basename(progress.current_file)

                    # Build the progress message
                    message = ""
                    if progress.total > 0:
                        message = f"{progress_percentage:.1f}%({progress.current}/{progress.total})"
                    else:
                        message = "0.0%(0/0)"

                    # Add file information if available
                    if file_path:
                        message += f" - {file_path}"
                    else:
                        message += " - Translating pages"

                    job.message = message

                    # Update total progress based on translation progress
                    # Translation is the remaining 50% of the total process
                    translation_weight = 0.5
                    # Calculate total progress: export (50%) + translation progress * 50%
                    job.total_progress = 50.0 + (
                        progress_percentage * translation_weight
                    )

                    logger.info(job.message)
                elif progress.status.value == "completed":
                    job.status = JobState.COMPLETED
                    job.message = f"100.0%({progress.total}/{progress.total}) - Translation completed"
                    job.translation_progress = 100.0
                    job.total_progress = 100.0
                    logger.info(job.message)
                elif progress.status.value == "failed":
                    job.status = JobState.FAILED
                    job.failure_reason = FailureReason.TRANSLATION_FAILED
                    job.message = f"0.0%(0/{progress.total}) - {progress.message or 'Translation failed'}"
                    job.total_progress = 0.0
                    logger.info(job.message)

        return translation_progress_callback

    def _format_page_id(self, page_id: str) -> str:
        """Format page ID to match Notion's expected format.

        Args:
            page_id: The page ID to format

        Returns:
            str: Formatted page ID in UUID format

        Raises:
            ValueError: If the page ID is invalid
        """
        try:
            # First transform to UUID format
            formatted_id = transform_block_id_to_uuidv4(page_id)

            # Validate the format
            if not validate_page_id(formatted_id):
                raise ValueError(f"Invalid page ID format: {page_id}")

            return formatted_id
        except Exception as e:
            logger.error(f"Error formatting page ID {page_id}: {str(e)}")
            raise ValueError(f"Invalid page ID: {page_id}")

    async def get_manuals(
        self, selected_solution: SolutionType = SolutionType.ZCP
    ) -> List[Union[Manual, Folder]]:
        """Retrieve the manual list from Notion and organize it into a tree structure.

        Args:
            selected_solution: The solution type selected by the user in the frontend (defaults to ZCP)

        Returns:
            List[Union[Manual, Folder]]: A hierarchical list of manuals and folders

        Raises:
            ValueError: If the root page ID is invalid or not configured
        """
        try:
            # Get the root page ID for the selected solution
            root_page_id = self.root_page_ids.get(selected_solution)
            if not root_page_id:
                error_msg = f"No root page ID configured for solution {selected_solution.value}. Check environment variables."
                logger.error(error_msg)
                logger.error(f"Available solutions: {list(self.root_page_ids.keys())}")
                logger.error(
                    f"Environment variable {selected_solution.value.upper()}_ROOT_PAGE_ID is not set"
                )
                raise ValueError(error_msg)

            # Format and validate the root page ID
            try:
                formatted_root_id = self._format_page_id(root_page_id)
            except ValueError as e:
                error_msg = f"Invalid root page ID for solution {selected_solution.value}: {str(e)}"
                logger.error(error_msg)
                raise ValueError(error_msg)

            # Create a separate exporter instance for this request
            # This allows concurrent requests to use their own exporters
            request_exporter = NotionPageExporter(
                notion_token=self.notion_token,
                root_page_id=formatted_root_id,
                root_output_dir="repo",
            )

            logger.info(
                f"Using root page ID for {selected_solution.value}: {formatted_root_id}"
            )

            # Get all nodes from the request-specific exporter
            # Run the synchronous get_tree_nodes method in a thread pool to avoid blocking
            try:
                # Use a thread pool to run the synchronous get_tree_nodes method
                # This prevents blocking the event loop for other requests
                nodes = await asyncio.to_thread(request_exporter.get_tree_nodes)

                if not nodes:
                    error_msg = f"No nodes returned for page ID: {formatted_root_id}"
                    logger.error(error_msg)
                    return []
                logger.info(f"Retrieved {len(nodes)} nodes from Notion")
            except Exception as e:
                error_msg = f"Error getting tree nodes: {str(e)}"
                logger.error(error_msg)
                return []

            return nodes

        except Exception as e:
            logger.error(f"Error retrieving manuals from Notion: {str(e)}")
            return []

    async def publish_manual(
        self,
        notion_page_id: str,
        selected_solution: Union[SolutionType, str],
        target_languages: Optional[Set[str]] = None,
        user_id: Optional[str] = None,
        job_id: Optional[str] = None,
    ) -> str:
        """Publish a manual by exporting it from Notion and translating it.

        Args:
            notion_page_id: The Notion page ID of the selected node to publish
            selected_solution: The solution type (ZCP/APIM/AMDP)
            target_languages: Optional set of target languages for translation
            user_id: Optional user ID to associate with notifications
            job_id: Optional job ID to use (if one was already created)

        Returns:
            str: The job ID for tracking the publication progress

        Raises:
            ValueError: If the notion_page_id is invalid
        """
        # Get the job ID if it already exists in active_jobs
        # We process previously queued jobs first

        # Handle None value for selected_solution
        if selected_solution is None:
            if not job_id:
                job_id = str(uuid.uuid4())

            self.active_jobs[job_id] = PublishStatus(
                job_id=job_id,
                notion_page_id=notion_page_id,
                status=JobState.FAILED,
                message="Solution type cannot be None",
                failure_reason=FailureReason.EXPORT_FAILED,
            )
            return job_id

        # Convert string to SolutionType if needed
        if isinstance(selected_solution, str):
            try:
                selected_solution = SolutionType(selected_solution.lower())
            except ValueError:
                # Handle invalid solution type
                if not job_id:
                    job_id = str(uuid.uuid4())

                self.active_jobs[job_id] = PublishStatus(
                    job_id=job_id,
                    notion_page_id=notion_page_id,
                    status=JobState.FAILED,
                    message=f"Invalid solution type: {selected_solution}",
                    failure_reason=FailureReason.EXPORT_FAILED,
                )
                return job_id

        # If no job_id was provided, check active jobs or create new one
        if not job_id:
            # Find the job ID from the active jobs
            # This allows us to continue a job that was created in the background tasks
            for jid, job in self.active_jobs.items():
                # Check for jobs that were just queued and are waiting to be processed
                if (
                    job.status == JobState.STARTED
                    and job.notion_page_id == notion_page_id
                ):
                    job_id = jid
                    break
                # Also continue any job that matches this request and is still in progress
                elif (
                    job.notion_page_id == notion_page_id
                    and job.solution == selected_solution.value
                    and job.status not in [JobState.COMPLETED, JobState.FAILED]
                ):
                    job_id = jid
                    break

            # If no job found, create a new one
            if not job_id:
                job_id = str(uuid.uuid4())
                self.active_jobs[job_id] = PublishStatus(
                    job_id=job_id,
                    notion_page_id=notion_page_id,
                    solution=selected_solution.value,
                    status=JobState.STARTED,
                    message="Starting publication process",
                    progress=0.0,
                )
            else:
                # Make sure the job exists and is properly initialized
                if job_id not in self.active_jobs:
                    self.active_jobs[job_id] = PublishStatus(
                        job_id=job_id,
                        notion_page_id=notion_page_id,
                        solution=selected_solution.value,
                        status=JobState.STARTED,
                        message="Starting publication process",
                        progress=0.0,
                    )
                elif not self.active_jobs[job_id].notion_page_id:
                    # Update the job with appropriate details if not already set
                    self.active_jobs[job_id].notion_page_id = notion_page_id
                    self.active_jobs[job_id].solution = selected_solution.value

        # Store a job context for use in callbacks
        self._current_job_context = {"job_id": job_id}

        # Create a job-specific repository path
        job_repo_path = os.path.join(self.repo_path, job_id)

        # Store the original repo path
        original_repo_path = self.repo_path

        try:
            # Update the repo path for this job
            self.repo_path = Path(job_repo_path).absolute()

            # Log the updated path
            logger.info(f"Created job-specific repository path: {self.repo_path}")

            # Make sure the job directory exists
            os.makedirs(job_repo_path, exist_ok=True)

            # Format the notion page ID
            formatted_page_id = notion_page_id.replace("-", "")
            notion_page_id = formatted_page_id
            # Check and prepare repository
            self.active_jobs[job_id].status = JobState.CHECKING_REPO
            self.active_jobs[job_id].message = "Checking repository status"

            if not await self._ensure_repository():
                # Repository check failed
                self.repo_path = original_repo_path
                return job_id

            # Clean up old files before export
            try:
                await self._cleanup_old_files(selected_solution)
                logger.info("Cleaned up old files before export")
            except Exception as e:
                logger.error(f"Failed to clean up old files: {str(e)}")
                self.active_jobs[job_id].status = JobState.FAILED
                self.active_jobs[job_id].failure_reason = FailureReason.EXPORT_FAILED
                self.active_jobs[job_id].message = "Failed to clean up old files"
                # Reset repo path to original
                self.repo_path = original_repo_path
                return job_id

            # Export from Notion
            self.active_jobs[job_id].status = JobState.EXPORTING
            self.active_jobs[job_id].message = "Initializing export from Notion..."
            self.active_jobs[job_id].export_progress = 0.0

            # Log callback creation for consistency with export callback
            logger.info(f"Creating export progress callback for job: {job_id}")

            # Call the dedicated export method
            export_success, export_path, mdx_files = await self.export_repository(
                notion_page_id=notion_page_id,
                output_dir=str(self.repo_path),
                selected_solution=selected_solution,
                job_id=job_id,
            )

            if not export_success:
                self.active_jobs[job_id].status = JobState.FAILED
                self.active_jobs[job_id].failure_reason = FailureReason.EXPORT_FAILED
                self.active_jobs[job_id].message = "Export failed, see logs for details"
                # Reset repo path to original
                self.repo_path = original_repo_path
                return job_id

            # Update job status with file counts
            self.active_jobs[
                job_id
            ].export_files = mdx_files  # Store original export files count
            self.active_jobs[job_id].export_progress = 100.0
            self.active_jobs[job_id].total_progress = 50.0  # Export is 50% complete
            self.active_jobs[
                job_id
            ].message = f"Successfully exported {mdx_files} MDX files"
            logger.info(f"Successfully exported {mdx_files} MDX files")

            # Ensure all required images are available for translation
            source_path = os.path.join(
                self.repo_path, self.source_dir, selected_solution.value.lower()
            )
            await self._ensure_images_for_translations(
                source_dir=source_path,
                target_languages=target_languages or self.target_languages,
                selected_solution=selected_solution,
            )

            # Translate the content
            self.active_jobs[job_id].status = JobState.TRANSLATING
            self.active_jobs[job_id].message = "Starting translation..."
            self.active_jobs[job_id].translation_progress = 0.0

            # Get the source path to translate (path to the specific manual being published)
            source_path = os.path.join(
                self.repo_path, self.source_dir, selected_solution.value.lower()
            )

            logger.info(f"Starting translation from {source_path}")

            # Log callback creation for consistency with export callback
            logger.info(f"Creating translation progress callback for job: {job_id}")

            # Translate the manual
            try:
                translation_success = await self.translate_repository(
                    source_path=source_path,
                    target_dir=self.target_dir,
                    target_languages=target_languages or self.target_languages,
                    selected_solution=selected_solution.value,
                    job_id=job_id,
                )

                if translation_success:
                    # Push changes to GitHub repository
                    self.active_jobs[job_id].status = JobState.PUSHING
                    self.active_jobs[
                        job_id
                    ].message = "Pushing changes to GitHub repository..."

                    # Call the _push_changes method to push to GitHub
                    push_success = await self._push_changes()

                    if push_success:
                        # Update job status to completed
                        self.active_jobs[job_id].status = JobState.COMPLETED
                        self.active_jobs[
                            job_id
                        ].message = "Manual published successfully and pushed to GitHub"
                        self.active_jobs[job_id].total_progress = 100.0
                        self.active_jobs[job_id].translation_progress = 100.0

                        # Create notification for successful completion
                        if user_id:
                            notification = Notification(
                                id=str(uuid.uuid4()),
                                user_id=user_id,
                                title="Manual Publication Complete",
                                message=f"The manual for '{selected_solution.value}' has been published successfully and pushed to GitHub.",
                                type=NotificationType.SUCCESS,
                                created_at=datetime.now(),
                                job_id=job_id,
                            )
                            await self.add_notification(notification)
                    else:
                        # Update job status to failed for push
                        self.active_jobs[job_id].status = JobState.FAILED
                        self.active_jobs[
                            job_id
                        ].message = (
                            "Translation successful but failed to push to GitHub"
                        )
                        self.active_jobs[
                            job_id
                        ].failure_reason = FailureReason.GIT_OPERATION_FAILED
                else:
                    self.active_jobs[job_id].status = JobState.FAILED
                    self.active_jobs[
                        job_id
                    ].message = "Translation failed, see logs for details"
                    self.active_jobs[
                        job_id
                    ].failure_reason = FailureReason.TRANSLATION_FAILED
            except Exception as e:
                logger.error(f"Error during translation: {str(e)}")
                self.active_jobs[job_id].status = JobState.FAILED
                self.active_jobs[
                    job_id
                ].failure_reason = FailureReason.TRANSLATION_FAILED
                self.active_jobs[job_id].message = f"Translation failed: {str(e)}"

        except Exception as e:
            logger.error(f"Error during publication process: {str(e)}")
            self.active_jobs[job_id].status = JobState.FAILED
            self.active_jobs[job_id].message = f"Publication failed: {str(e)}"
            self.active_jobs[job_id].failure_reason = FailureReason.UNKNOWN

        finally:
            # Always reset repo path to original
            self.repo_path = original_repo_path

            # Clean up job context
            if hasattr(self, "_current_job_context"):
                delattr(self, "_current_job_context")

        return job_id

    async def get_job_status(self, job_id: str) -> Optional[PublishStatus]:
        """Get the status of a publishing job.

        Args:
            job_id: The ID of the job to check

        Returns:
            Optional[PublishStatus]: The job status if found, None otherwise
        """
        return self.active_jobs.get(job_id)

    async def _cleanup_old_files(self, selected_solution: SolutionType) -> None:
        """Clean up old files before export.

        Args:
            selected_solution: The solution type being processed
        """
        try:
            # Define a function to perform file cleanup operations
            def cleanup_directory(directory):
                if not os.path.exists(directory):
                    return

                for item in os.listdir(directory):
                    item_path = os.path.join(directory, item)
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        import shutil

                        shutil.rmtree(item_path)
                logger.info(f"Cleaned up directory: {directory}")

            # Clean up source directory
            source_dir = os.path.join(
                self.repo_path, self.source_dir, selected_solution.value.lower()
            )
            await asyncio.to_thread(cleanup_directory, source_dir)

            # Clean up static image directory for the specific solution
            static_img_dir = os.path.join(
                self.repo_path, "static", "img", selected_solution.value.lower()
            )
            await asyncio.to_thread(cleanup_directory, static_img_dir)

            # Clean up target directories for each language
            for lang in self.target_languages:
                target_dir = os.path.join(
                    self.repo_path,
                    self.target_dir,
                    lang,
                    f"docusaurus-plugin-content-docs-{selected_solution.value.lower()}",
                    "current",
                )
                await asyncio.to_thread(cleanup_directory, target_dir)

        except Exception as e:
            logger.error(f"Error cleaning up old files: {str(e)}")
            raise

    async def _ensure_repository(self) -> bool:
        """Ensure repository exists and is up to date.
        Returns True if successful, False otherwise."""
        try:
            repo_path = Path(self.repo_path)
            should_clone = False

            # Function to check if a directory is a valid git repository
            def is_valid_git_repo(path):
                try:
                    git.Repo(path)
                    return True
                except git.exc.InvalidGitRepositoryError:
                    return False

            # Check if directory exists and is not empty
            if not repo_path.exists():
                should_clone = True
            else:
                # Check if directory is empty
                if not any(repo_path.iterdir()):
                    should_clone = True
                else:
                    # Check if it's a valid git repository (potentially blocking operation)
                    try:
                        is_valid = await asyncio.to_thread(is_valid_git_repo, repo_path)
                        if not is_valid:
                            should_clone = True
                    except Exception:
                        should_clone = True

            if should_clone:
                # Update job status for cloning
                if hasattr(self, "_current_job_context"):
                    job_id = self._current_job_context["job_id"]
                    if job_id in self.active_jobs:
                        current_job = self.active_jobs[job_id]
                        # Create a dictionary of current values excluding the ones we want to update
                        current_values = current_job.model_dump()
                        current_values.update(
                            {
                                "status": JobState.CLONING,
                                "message": f"Cloning repository from {self.github_repo_url}",
                            }
                        )
                        updated_job = PublishStatus(**current_values)
                        self.active_jobs[job_id] = updated_job

                logger.info(f"Cloning repository from {self.github_repo_url}")

                # Remove directory if it exists but is empty or not a valid repo
                if repo_path.exists():
                    import shutil

                    await asyncio.to_thread(shutil.rmtree, repo_path)

                # Clone the entire repository without modifying anything (blocking operation)
                await asyncio.to_thread(
                    git.Repo.clone_from, self.github_repo_url, repo_path
                )

                # Only ensure our working directories exist without affecting others
                work_dirs = [
                    os.path.join(self.repo_path, self.source_dir),
                    os.path.join(self.repo_path, self.target_dir),
                ]

                # Create directories in a non-blocking way
                for directory in work_dirs:
                    if not os.path.exists(directory):
                        await asyncio.to_thread(os.makedirs, directory, exist_ok=True)
                        logger.info(f"Created working directory: {directory}")

                return True

            # If we don't need to clone, update existing repository
            # Update job status for pulling
            if hasattr(self, "_current_job_context"):
                job_id = self._current_job_context["job_id"]
                if job_id in self.active_jobs:
                    current_job = self.active_jobs[job_id]
                    # Create a dictionary of current values excluding the ones we want to update
                    current_values = current_job.model_dump()
                    current_values.update(
                        {
                            "status": JobState.PULLING,
                            "message": "Updating repository (git pull)",
                        }
                    )
                    updated_job = PublishStatus(**current_values)
                    self.active_jobs[job_id] = updated_job

            logger.info("Repository exists, checking develop branch")

            # Function to update the repository
            def update_repo():
                try:
                    repo = git.Repo(repo_path)
                    origin = repo.remotes.origin

                    # Fetch all branches first (required for proper reference handling)
                    logger.info("Fetching branches")
                    origin.fetch()

                    # Check if develop branch exists in remote
                    remote_refs = [ref.name for ref in repo.refs]
                    remote_develop_exists = "origin/develop" in remote_refs

                    # If remote develop doesn't exist, try to create it from main/master
                    if not remote_develop_exists:
                        # Check if main or master exists in remote
                        if "origin/main" in remote_refs:
                            base_branch = "main"
                        elif "origin/master" in remote_refs:
                            base_branch = "master"
                        else:
                            logger.error(
                                "Neither develop, main, nor master branch exists in remote"
                            )
                            raise ValueError("No valid base branch found in remote")

                        # Create and push develop branch from base branch
                        logger.info(f"Creating develop branch from {base_branch}")
                        repo.git.checkout("-b", "develop", f"origin/{base_branch}")
                        repo.git.push("--set-upstream", "origin", "develop")
                        remote_develop_exists = True

                    # Now handle local develop branch
                    if "develop" not in repo.heads:
                        # Create local develop branch tracking remote develop
                        logger.info(
                            "Creating local develop branch tracking origin/develop"
                        )
                        develop = repo.create_head("develop", "origin/develop")
                        develop.set_tracking_branch(origin.refs.develop)
                    else:
                        develop = repo.heads["develop"]
                        # Ensure local develop is tracking remote develop
                        if (
                            not develop.tracking_branch()
                            or develop.tracking_branch().name != "origin/develop"
                        ):
                            develop.set_tracking_branch(origin.refs.develop)

                    # Switch to develop branch if not already on it
                    if repo.active_branch.name != "develop":
                        logger.info("Switching to develop branch")
                        develop.checkout()

                    # Reset local branch to match remote if they're out of sync
                    logger.info("Synchronizing with remote develop branch")
                    repo.git.reset("--hard", "origin/develop")

                    # Pull latest changes
                    logger.info("Pulling latest changes from develop branch")
                    repo.git.pull("origin", "develop")

                    return True
                except git.exc.GitCommandError as e:
                    logger.error(f"Git command failed: {str(e)}")
                    raise e

            # Run update_repo in a thread to avoid blocking
            try:
                return await asyncio.to_thread(update_repo)
            except Exception as e:
                logger.error(f"Repository operation failed: {str(e)}")
                if hasattr(self, "_current_job_context"):
                    job = self.active_jobs[self._current_job_context["job_id"]]
                    job.status = JobState.FAILED
                    job.failure_reason = FailureReason.GIT_OPERATION_FAILED
                    job.message = f"Repository operation failed: {str(e)}"
                return False

        except Exception as e:
            logger.error(f"Repository operation failed: {str(e)}")
            if hasattr(self, "_current_job_context"):
                job = self.active_jobs[self._current_job_context["job_id"]]
                job.status = JobState.FAILED
                job.failure_reason = FailureReason.REPO_ACCESS
                job.message = f"Repository operation failed: {str(e)}"
            return False

    async def _commit_export_changes(self, message: str) -> bool:
        """Commit changes after export phase."""
        try:
            if hasattr(self, "_current_job_context"):
                job = self.active_jobs[self._current_job_context["job_id"]]
                job.status = JobState.EXPORT_COMMIT
                job.message = "Committing exported files"

            # Define a function to perform all git operations in a thread
            def perform_git_operations():
                try:
                    repo = git.Repo(self.repo_path)

                    # Ensure we're on develop branch
                    if repo.active_branch.name != "develop":
                        logger.error("Not on develop branch")
                        raise ValueError("Not on develop branch")

                    # Add both documentation and static files
                    repo.git.add(os.path.join(self.source_dir, "*"))
                    repo.git.add("static")  # Add the entire static directory

                    # Check if there are any changes to commit
                    if repo.is_dirty(untracked_files=True):
                        repo.index.commit(f"docs: {message}")
                        logger.info(
                            "Committed changes to documentation and static files"
                        )
                    else:
                        logger.info("No changes to commit")

                    return True
                except Exception as e:
                    logger.error(f"Error in git operations: {str(e)}")
                    return False

            # Run git operations in a thread pool
            return await asyncio.to_thread(perform_git_operations)

        except Exception as e:
            logger.error(f"Failed to commit export changes: {str(e)}")
            if hasattr(self, "_current_job_context"):
                job = self.active_jobs[self._current_job_context["job_id"]]
                job.status = JobState.FAILED
                job.failure_reason = FailureReason.GIT_OPERATION_FAILED
                job.message = f"Failed to commit export changes: {str(e)}"
            return False

    async def _commit_translation_changes(self, message: str) -> bool:
        """Commit changes after translation phase."""
        try:
            if hasattr(self, "_current_job_context"):
                job = self.active_jobs[self._current_job_context["job_id"]]
                job.status = JobState.TRANSLATION_COMMIT
                job.message = "Committing translated files"

            # Define a function to perform all git operations in a thread
            def perform_git_operations():
                try:
                    repo = git.Repo(self.repo_path)

                    # Ensure we're on develop branch
                    if repo.active_branch.name != "develop":
                        logger.error("Not on develop branch")
                        raise ValueError("Not on develop branch")

                    repo.git.add(os.path.join(self.target_dir, "*"))
                    repo.index.commit(f"i18n: {message}")
                    return True
                except Exception as e:
                    logger.error(f"Error in git operations: {str(e)}")
                    return False

            # Run git operations in a thread pool
            return await asyncio.to_thread(perform_git_operations)

        except Exception as e:
            logger.error(f"Failed to commit translation changes: {str(e)}")
            if hasattr(self, "_current_job_context"):
                job = self.active_jobs[self._current_job_context["job_id"]]
                job.status = JobState.FAILED
                job.failure_reason = FailureReason.GIT_OPERATION_FAILED
                job.message = f"Failed to commit translation changes: {str(e)}"
            return False

    async def _push_changes(self) -> bool:
        """Push all changes to remote repository."""
        try:
            if hasattr(self, "_current_job_context"):
                job = self.active_jobs[self._current_job_context["job_id"]]
                job.status = JobState.PUSHING
                job.message = "Pushing changes to remote repository"

            # Define a function to perform all git operations in a thread
            def perform_git_operations():
                try:
                    repo = git.Repo(self.repo_path)

                    # Log current state for debugging
                    logger.info(f"Current repo path: {self.repo_path}")
                    logger.info(f"Current branch: {repo.active_branch.name}")

                    # First, ensure we're on the develop branch
                    if repo.active_branch.name != "develop":
                        logger.info("Switching to develop branch")
                        repo.heads.develop.checkout()

                    # Force add all relevant directories to ensure all changes are tracked
                    logger.info("Adding source directory files")
                    repo.git.add(os.path.join(self.source_dir, "*"), force=True)

                    logger.info("Adding target (i18n) directory files")
                    repo.git.add(os.path.join(self.target_dir, "*"), force=True)

                    logger.info("Adding static directory files")
                    repo.git.add("static", force=True)

                    # Check if there are changes to commit
                    diff_index = repo.index.diff(repo.head.commit)
                    unstaged = repo.index.diff(None)
                    untracked = repo.untracked_files

                    has_changes = (
                        len(diff_index) > 0 or len(unstaged) > 0 or len(untracked) > 0
                    )
                    logger.info(
                        f"Changes detected: staged={len(diff_index)}, unstaged={len(unstaged)}, untracked={len(untracked)}"
                    )

                    if has_changes:
                        # Commit all changes with a meaningful message
                        logger.info("Committing changes")
                        commit = repo.index.commit(
                            "docs: Update documentation and translations"
                        )
                        logger.info(f"Committed changes with hash: {commit.hexsha[:7]}")
                    else:
                        logger.info("No changes to commit")

                    # Always attempt to push - there might be commits that haven't been pushed yet
                    logger.info("Pushing changes to remote repository")

                    # Set target branch
                    target_branch = "develop"

                    # First make sure we're up to date with remote
                    logger.info("Fetching latest changes from remote")
                    origin = repo.remote(name="origin")
                    fetch_info = origin.fetch()
                    logger.info(f"Fetch info: {fetch_info}")

                    # Try to push
                    try:
                        logger.info(f"Pushing develop branch to origin/{target_branch}")
                        # Use force=True to override any conflicts
                        push_info = origin.push(
                            refspec=f"develop:{target_branch}", force=True
                        )

                        # Log push info for debugging
                        for info in push_info:
                            logger.info(f"Push result: {info.summary}")
                            if info.flags & info.ERROR:
                                logger.error(f"Push error: {info.summary}")
                                return False

                        logger.info("Push completed successfully")
                        return True
                    except git.exc.GitCommandError as e:
                        error_msg = str(e)
                        logger.error(f"Git command error during push: {error_msg}")

                        # Specific error handling
                        if (
                            "authentication failed" in error_msg.lower()
                            or "403" in error_msg
                        ):
                            logger.error(
                                "Git authentication failed. Please check Git credentials or SSH keys."
                            )
                            # Suggest creating a credential helper or using SSH
                            logger.info(
                                "Try using SSH keys or git credential helper for authentication"
                            )
                        elif (
                            "rejected" in error_msg.lower()
                            and "non-fast-forward" in error_msg.lower()
                        ):
                            logger.error(
                                "Remote rejected non-fast-forward push. Try pulling latest changes first."
                            )

                        return False
                except Exception as e:
                    logger.error(f"Unexpected error during git operations: {str(e)}")
                    return False

            # Run git operations in a thread pool
            return await asyncio.to_thread(perform_git_operations)

        except Exception as e:
            logger.error(f"Failed to push changes: {str(e)}")
            if hasattr(self, "_current_job_context"):
                job = self.active_jobs[self._current_job_context["job_id"]]
                job.status = JobState.FAILED
                job.failure_reason = FailureReason.GIT_OPERATION_FAILED
                job.message = f"Failed to push changes: {str(e)}"
            return False

    def _create_export_progress_callback(self, job_id: str):
        """Create a progress callback for the export process for a specific job.

        This creates a synchronous callback because the NotionPageExporter expects a regular function callback.
        Unlike the translation callback, this uses a synchronous function signature.

        Args:
            job_id: The ID of the job to update progress for

        Returns:
            A callback function that can be passed to the exporter
        """
        # Note: This now directly accepts a job_id parameter similar to _create_translation_progress_callback
        # instead of relying on the _current_job_context

        def progress_callback(current: int, total: int, message: str = None):
            try:
                if job_id in self.active_jobs:
                    job = self.active_jobs[job_id]
                else:
                    logger.warning(f"Job {job_id} not found for progress callback")
                    return

                job = self.active_jobs[job_id]

                if total <= 0:
                    logger.warning(f"Invalid total ({total}) in progress callback")
                    return

                # Calculate progress percentage
                progress_percentage = round((current / total) * 100, 1)
                job.export_progress = progress_percentage

                # Update export_files
                job.export_files = current

                # Format the message with progress
                job.message = f"{progress_percentage:.1f}%({current}/{total})"

                # Add page-specific message if provided
                if message:
                    # Clean up the message to show only relevant part of the path
                    if "Exported page: " in message:
                        page_path = message.split("Exported page: ", 1)[1]

                        # Remove job directory and repository path information
                        # Get only the relevant document path
                        if "/repo/" in page_path:
                            # Try different methods to extract meaningful path
                            if "/" in page_path:
                                # Get either the last part of the path (file name) or preserve some path structure
                                parts = page_path.split("/")
                                if (
                                    len(parts) > 3
                                ):  # If we have a deep path, show last 2-3 components
                                    meaningful_path = (
                                        "/".join(parts[-3:])
                                        if len(parts) > 3
                                        else parts[-1]
                                    )
                                else:
                                    meaningful_path = parts[-1]  # Just the filename
                                job.message += f" - Exported page: {meaningful_path}"
                            else:
                                job.message += f" - Exported page: {page_path}"
                        # For relative paths or other formats
                        else:
                            job.message += f" - Exported page: {page_path}"
                    else:
                        job.message += f" - {message}"
                else:
                    job.message += f" - Exporting page {current}"

                # Update total progress based on export progress only
                # Export is 50% of the total process
                job.total_progress = round(progress_percentage * 0.5, 1)

                # Log the progress message
                logger.info(job.message)
            except Exception as e:
                # Don't crash the callback on error
                logger.error(f"Error in export progress callback: {str(e)}")

        return progress_callback

    async def translate_repository(
        self,
        source_path: str,
        target_dir: str | None,
        target_languages: list[str],
        selected_solution: str | None = None,
        job_id: str | None = None,
    ) -> bool:
        """Translate repository content to target languages.

        Args:
            source_path (str): Path to the source content (corresponds to selected Notion page)
            target_dir (str | None): Target directory for translations
            target_languages (list[str]): List of target languages to translate to
            selected_solution (str | None, optional): Selected solution type (ZCP, APIM, AMDP)
            job_id (str | None, optional): Current job ID for tracking progress

        Returns:
            bool: True if translation was successful, False otherwise
        """
        try:
            if not source_path or not target_languages:
                logger.error("Source path and target languages must be provided")
                return False

            # Get the solution type enum from string
            solution = (
                SolutionType(selected_solution.lower()) if selected_solution else None
            )
            if not solution:
                logger.error(f"Invalid solution type: {selected_solution}")
                return False

            # Log the actual paths we're working with for debugging
            logger.info(f"Starting translation from source path: {source_path}")
            logger.info(f"Selected solution: {solution.value}")

            # Set up the target directory
            if target_dir is None:
                target_dir = "i18n"

            # Create a job-specific translator instance with appropriate callback
            translation_progress_callback = None
            if job_id and job_id in self.active_jobs:
                translation_progress_callback = (
                    self._create_translation_progress_callback(job_id)
                )
                logger.info(f"Using progress tracking for job {job_id}")

            # Log the directories we're translating
            logger.info(f"Source directory: {source_path}")
            target_path = (
                os.path.join(self.repo_path, target_dir)
                if not os.path.isabs(target_dir)
                else target_dir
            )
            logger.info(f"Target directory: {target_path}")

            # Ensure images are available for translations
            # Copy images from static/img directory to ensure they're available for the translated content
            solution_img_dir = os.path.join(
                self.repo_path, "static", "img", solution.value.lower()
            )
            logger.info(f"Checking for images in: {solution_img_dir}")
            if os.path.exists(solution_img_dir):
                # Create any necessary image directories in the target path
                os.makedirs(
                    os.path.join(
                        self.repo_path, "static", "img", solution.value.lower()
                    ),
                    exist_ok=True,
                )

                # Log image files found
                image_count = 0
                for root, _, files in os.walk(solution_img_dir):
                    for file in files:
                        if file.lower().endswith(
                            (".png", ".jpg", ".jpeg", ".gif", ".svg")
                        ):
                            image_count += 1

                if image_count > 0:
                    logger.info(
                        f"Found {image_count} image files for solution {solution.value}"
                    )
                else:
                    logger.warning(
                        f"No image files found in {solution_img_dir}. This may cause missing images in translated content."
                    )
            else:
                logger.warning(
                    f"Image directory {solution_img_dir} does not exist. This may cause missing images in translated content."
                )

            # Create a dedicated translator for this task
            task_translator = MarkdownTranslator(
                progress_callback=translation_progress_callback
            )

            # Translate the exported content
            # The translator will handle the solution-specific directory structure
            result = await task_translator.translate_repository(
                source_path=source_path,  # Use the provided source path directly
                target_dir=target_path,
                target_languages=target_languages,
                selected_solution=solution.value,
            )

            # Enhanced result checking with better logging
            # Check if translation was successful
            if result:
                # First, log the actual result type and structure for debugging
                logger.info(f"Translation result type: {type(result)}")
                logger.info(
                    f"Translation result attributes: {dir(result) if hasattr(result, '__dir__') else 'No attributes'}"
                )

                # Method 1: Check for status attribute
                if hasattr(result, "status"):
                    status_value = getattr(result.status, "value", str(result.status))
                    logger.info(f"Translation status: {status_value}")

                    if (
                        status_value == "completed"
                        or "success" in status_value.lower()
                        or "complete" in status_value.lower()
                    ):
                        logger.info(
                            f"Translation completed successfully for job {job_id}"
                        )
                        return True

                # Method 2: Check for success indication in the result itself
                elif isinstance(result, bool) and result:
                    logger.info(f"Translation returned boolean True for job {job_id}")
                    return True

                # Method 3: Check for success in any string representation
                elif hasattr(result, "__str__"):
                    result_str = str(result).lower()
                    if "success" in result_str or "complete" in result_str:
                        logger.info(
                            f"Translation completed successfully for job {job_id}"
                        )
                        return True

                # If we get here, we couldn't positively confirm success, but the result exists
                # Log the error with more details
                error_msg = getattr(result, "message", "Unknown error")
                logger.error(
                    f"Translation result exists but success not confirmed: {error_msg}"
                )
                logger.error(f"Full result: {str(result)}")
                return False
            else:
                # If result is None or falsy
                logger.error("Translation failed: No result returned from translator")
                return False
        except Exception as e:
            logger.error(f"Error during translation: {str(e)}")
            return False

    def _find_node_by_path(
        self, nodes: list[Union[Manual, Folder]], target_path: str
    ) -> Union[Manual, Folder, None]:
        """Find a node (Manual or Folder) by its path in the manual structure.

        Args:
            nodes (list[Union[Manual, Folder]]): List of nodes to search
            target_path (str): Target path to find

        Returns:
            Union[Manual, Folder, None]: Found node or None if not found
        """
        for node in nodes:
            if isinstance(node, Manual):
                if node.path == target_path:
                    return node
            elif isinstance(node, Folder):
                # For folders, check children recursively
                if node.children:
                    found = self._find_node_by_path(node.children, target_path)
                    if found:
                        return found
        return None

    def _add_notification(
        self,
        type: NotificationType,
        title: str,
        message: str,
        solution: Optional[SolutionType] = None,
        user_id: Optional[str] = None,
    ):
        """Add a new notification."""
        notification = Notification(
            type=type,
            title=title,
            message=message,
            solution=solution,
            user_id=user_id,
        )
        self.notifications.append(notification)
        logger.info(
            f"Added notification: {notification.title} - {notification.message} for user: {user_id if user_id else 'all'}"
        )

        # Broadcast to all registered clients
        asyncio.create_task(self._broadcast_notification(notification))

        return notification

    async def _broadcast_notification(self, notification: Notification):
        """Broadcast a notification to all registered clients.

        Args:
            notification: The notification to broadcast
        """
        # Create a copy of the clients to avoid modification during iteration
        clients = list(self.notification_clients.items())

        for client_id, (queue, user_id) in clients:
            # Only send to clients with matching user_id or if notification has no user_id
            if (
                notification.user_id is None
                or user_id is None
                or notification.user_id == user_id
            ):
                try:
                    # Non-blocking put with a timeout
                    await asyncio.wait_for(queue.put(notification), timeout=1.0)
                except asyncio.TimeoutError:
                    logger.warning(f"Timeout broadcasting to client {client_id}")
                except Exception as e:
                    logger.error(f"Error broadcasting to client {client_id}: {str(e)}")
                    # Remove client on error
                    await self.unregister_notification_client(client_id)

    async def register_notification_client(
        self, queue: asyncio.Queue, user_id: Optional[str] = None
    ) -> str:
        """Register a new client for notification streaming.

        Args:
            queue: An asyncio Queue where notifications will be sent
            user_id: Optional user ID to filter notifications

        Returns:
            A unique client ID that can be used to unregister
        """
        client_id = str(uuid.uuid4())
        self.notification_clients[client_id] = (queue, user_id)
        logger.info(f"Registered notification client {client_id} for user {user_id}")
        return client_id

    async def unregister_notification_client(self, client_id: str) -> bool:
        """Unregister a client from notification streaming.

        Args:
            client_id: The client ID to unregister

        Returns:
            True if the client was unregistered, False if not found
        """
        if client_id in self.notification_clients:
            queue, _ = self.notification_clients.pop(client_id)
            # Signal to the client that it should stop listening
            try:
                await queue.put(None)
            except Exception:
                pass  # Ignore errors when client is already gone

            logger.info(f"Unregistered notification client {client_id}")
            return True
        return False

    async def unregister_all_clients(self):
        """Unregister all notification clients."""
        client_ids = list(self.notification_clients.keys())
        for client_id in client_ids:
            await self.unregister_notification_client(client_id)

        logger.info(f"Unregistered all {len(client_ids)} notification clients")

    async def get_notifications(
        self,
        limit: int = 50,
        include_read: bool = False,
        user_id: Optional[str] = None,
        latest_only: bool = False,
    ) -> Union[List[Notification], Optional[Notification]]:
        """Get recent notifications.

        Args:
            limit: Maximum number of notifications to return
            include_read: Whether to include read notifications
            user_id: Filter notifications by user_id
            latest_only: If True, return only the latest notification as a single object

        Returns:
            Either a list of notifications or a single latest notification (if latest_only=True)
        """
        # Filter by read status and user_id
        filtered = [
            n
            for n in self.notifications
            if (include_read or not n.is_read)
            and (user_id is None or n.user_id == user_id or n.user_id is None)
        ]

        # Sort by creation time (newest first)
        sorted_notifications = sorted(
            filtered, key=lambda x: x.created_at, reverse=True
        )

        # Return only the latest notification if requested
        if latest_only and sorted_notifications:
            return sorted_notifications[0]
        elif latest_only:
            return None

        # Otherwise return a list limited by the limit parameter
        return sorted_notifications[:limit]

    async def mark_notification_read(self, notification_id: str) -> bool:
        """Mark a notification as read."""
        for notification in self.notifications:
            if notification.id == notification_id:
                notification.is_read = True
                return True
        return False

    async def clear_notifications(self) -> None:
        """Clear all notifications."""
        self.notifications = []

    async def export_repository(
        self,
        notion_page_id: str,
        output_dir: str,
        selected_solution: SolutionType,
        job_id: Optional[str] = None,
    ) -> Tuple[bool, Optional[str], Optional[int]]:
        """Export repository content from Notion.

        Args:
            notion_page_id (str): The Notion page ID to export
            output_dir (str): Directory to place exported files
            selected_solution (SolutionType): The solution type (ZCP/APIM/AMDP)
            job_id (Optional[str], optional): Current job ID for tracking progress

        Returns:
            Tuple[bool, Optional[str], Optional[int]]:
                - Success status
                - Path to exported content
                - Number of MDX files exported

        Raises:
            ValueError: If notion_page_id is invalid
        """
        if not notion_page_id:
            logger.error("Notion page ID must be provided")
            return False, None, 0

        try:
            # Format the notion page ID
            formatted_page_id = notion_page_id.replace("-", "")

            # Log the starting of export
            logger.info(f"Starting export from Notion page {formatted_page_id}")
            logger.info(f"Selected solution: {selected_solution.value}")

            # Create a new exporter instance for this specific export task
            task_exporter = NotionPageExporter(
                notion_token=self.notion_token,
                root_page_id=formatted_page_id,
                root_output_dir=str(
                    self.repo_path
                ),  # Use job-specific path already set in publish_manual
            )

            # Create export progress callback for this specific job
            export_progress_callback = None
            if job_id and job_id in self.active_jobs:
                export_progress_callback = self._create_export_progress_callback(job_id)
                logger.info(f"Using progress tracking for job {job_id}")

            # Log the directories we're exporting to
            logger.info(f"Output directory: {self.repo_path}")

            # Export the content
            export_path = await asyncio.to_thread(
                task_exporter.markdownx,  # Use markdownx for MDX file support
                page_id=formatted_page_id,
                include_subpages=True,
                progress_callback=export_progress_callback,  # Use the job-specific callback
            )

            # Enhanced result checking with better logging
            logger.info(f"Export result path: {export_path}")

            if not export_path:
                logger.error(
                    f"Export failed: No path returned from exporter for page {formatted_page_id}"
                )
                return False, None, 0

            if not os.path.exists(export_path):
                logger.error(
                    f"Export failed: Path returned ({export_path}) does not exist"
                )
                return False, None, 0

            # Verify the exported files
            if job_id and job_id in self.active_jobs:
                self.active_jobs[job_id].message = "Verifying exported files..."

            export_dir = os.path.dirname(export_path)

            # Function to count MDX files
            def count_mdx_files(directory):
                mdx_count = 0
                for root, _, files in os.walk(directory):
                    for file in files:
                        if file.endswith(".mdx"):
                            mdx_count += 1
                            logger.info(f"Found MDX file: {os.path.join(root, file)}")
                return mdx_count

            if os.path.exists(export_dir):
                source_dir = os.path.join(
                    self.repo_path, self.source_dir, selected_solution.value.lower()
                )
                # Run file counting in a separate thread to avoid blocking
                mdx_files = await asyncio.to_thread(count_mdx_files, source_dir)

                logger.info(f"Successfully exported {mdx_files} MDX files")
                return True, export_path, mdx_files

            logger.error("Export directory does not exist after export")
            return False, None, 0

        except Exception as e:
            logger.error(f"Error during export: {str(e)}")
            return False, None, 0

    async def _ensure_images_for_translations(
        self,
        source_dir: str,
        target_languages: list[str],
        selected_solution: SolutionType,
    ) -> bool:
        """Make sure all required images are available for translations.
        This copies images from the source or master repository to ensure they're available for the translated content.

        Args:
            source_dir: Path to the source directory containing MDX files
            target_languages: List of target languages
            selected_solution: The solution type (ZCP/APIM/AMDP)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            solution_value = selected_solution.value.lower()

            # Source image directory (where images should be)
            source_img_dir = os.path.join(
                self.repo_path, "static", "img", solution_value
            )
            logger.info(f"Checking for images in: {source_img_dir}")

            # Ensure source image directory exists
            if not os.path.exists(source_img_dir):
                os.makedirs(source_img_dir, exist_ok=True)
                logger.info(f"Created missing image directory: {source_img_dir}")

            # Find all MDX files in the source directory
            mdx_files = []
            for root, _, files in os.walk(source_dir):
                for file in files:
                    if file.endswith(".mdx"):
                        mdx_files.append(os.path.join(root, file))

            logger.info(
                f"Found {len(mdx_files)} MDX files to check for image references"
            )

            # Extract image references from MDX files
            import re

            image_refs = set()

            # Pattern to match markdown image references like ![alt](path/to/image.png)
            # and HTML img tags like <img src="path/to/image.png">
            md_pattern = r"!\[[^\]]*\]\(([^)]+)\)"
            html_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'

            for mdx_file in mdx_files:
                try:
                    with open(mdx_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Find all markdown image references
                    md_matches = re.findall(md_pattern, content)
                    for match in md_matches:
                        if match.startswith("static/"):
                            image_refs.add(match)

                    # Find all HTML img tags
                    html_matches = re.findall(html_pattern, content)
                    for match in html_matches:
                        if match.startswith("static/"):
                            image_refs.add(match)

                except Exception as e:
                    logger.error(f"Error reading MDX file {mdx_file}: {str(e)}")

            logger.info(f"Found {len(image_refs)} unique image references in MDX files")

            # Verify all referenced images exist
            missing_images = []
            for img_ref in image_refs:
                abs_path = os.path.join(self.repo_path, img_ref)
                if not os.path.exists(abs_path):
                    missing_images.append(img_ref)

            # Handle missing images - create directories and placeholder images
            if missing_images:
                logger.warning(
                    f"Found {len(missing_images)} missing images referenced in MDX files"
                )

                # Try to create placeholder images for missing images
                import shutil
                from PIL import Image, ImageDraw, ImageFont

                # Create a placeholder image
                def create_placeholder_image(path, ref):
                    try:
                        # Ensure the directory exists
                        os.makedirs(os.path.dirname(path), exist_ok=True)

                        # Create a simple image with text indicating it's a placeholder
                        width, height = 400, 300
                        image = Image.new("RGB", (width, height), color=(245, 245, 245))
                        draw = ImageDraw.Draw(image)

                        # Draw a border
                        draw.rectangle(
                            [(0, 0), (width - 1, height - 1)], outline=(200, 200, 200)
                        )

                        # Add text
                        try:
                            # Try to load a font, using default if not available
                            font = ImageFont.truetype("Arial", 16)
                        except IOError:
                            # Use default font if Arial not available
                            font = ImageFont.load_default()

                        # Add text explaining the image is missing
                        message = f"Placeholder Image\n\nOriginal image not found\n{os.path.basename(ref)}"

                        # Handle both older and newer versions of PIL
                        try:
                            # Newer PIL versions
                            text_width = draw.textlength(message, font=font)
                            position = ((width - text_width) / 2, height / 3)
                            draw.text(
                                position, message, fill=(100, 100, 100), font=font
                            )
                        except AttributeError:
                            # Older PIL versions don't have textlength
                            # Just center approximately
                            position = (width / 4, height / 3)
                            draw.text(
                                position, message, fill=(100, 100, 100), font=font
                            )

                        # Save the image
                        image.save(path)
                        logger.info(f"Created placeholder image: {path}")
                        return True
                    except Exception as e:
                        logger.error(
                            f"Error creating placeholder image {path}: {str(e)}"
                        )
                        return False

                # Try to recover from main repository if available
                main_repo_path = os.path.join(os.path.dirname(self.repo_path), "repo")
                recovered_count = 0
                placeholder_count = 0

                for img_ref in missing_images:
                    abs_path = os.path.join(self.repo_path, img_ref)

                    # First, try to recover from main repository if it exists
                    main_repo_img_path = os.path.join(main_repo_path, img_ref)
                    if os.path.exists(main_repo_path) and os.path.exists(
                        main_repo_img_path
                    ):
                        # Directory exists, copy from there
                        try:
                            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
                            shutil.copy(main_repo_img_path, abs_path)
                            logger.info(
                                f"Recovered missing image from main repo: {img_ref}"
                            )
                            recovered_count += 1
                        except Exception as e:
                            logger.error(
                                f"Error copying image from main repo: {str(e)}"
                            )
                            # If copy fails, create placeholder
                            if create_placeholder_image(abs_path, img_ref):
                                placeholder_count += 1
                    else:
                        # Main repo image not found, create placeholder
                        if create_placeholder_image(abs_path, img_ref):
                            placeholder_count += 1

                logger.info(
                    f"Image recovery summary: recovered {recovered_count}, created {placeholder_count} placeholders"
                )
            else:
                logger.info("All referenced images exist in the repository")

            # For each target language in translations, ensure the static directory is available at the repository root
            # This is important for Docusaurus to find images from translated content
            for lang in target_languages:
                # Check if the target language's docusaurus directory exists
                target_lang_dir = os.path.join(
                    self.repo_path,
                    self.target_dir,
                    lang,
                    f"docusaurus-plugin-content-docs-{solution_value}",
                    "current",
                )

                # If this directory exists, it means we need to make sure images are accessible
                if os.path.exists(target_lang_dir):
                    logger.info(
                        f"Found translated content for {lang}, ensuring images are accessible"
                    )

                    # Make sure static directory exists at repo root
                    static_dir = os.path.join(self.repo_path, "static")
                    if not os.path.exists(static_dir):
                        os.makedirs(static_dir, exist_ok=True)
                        logger.info(f"Created static directory: {static_dir}")

                    # Make sure static/img directory exists
                    img_dir = os.path.join(static_dir, "img")
                    if not os.path.exists(img_dir):
                        os.makedirs(img_dir, exist_ok=True)
                        logger.info(f"Created static/img directory: {img_dir}")

                    # Make sure static/img/solution directory exists
                    solution_img_dir = os.path.join(img_dir, solution_value)
                    if not os.path.exists(solution_img_dir):
                        os.makedirs(solution_img_dir, exist_ok=True)
                        logger.info(
                            f"Created static/img/{solution_value} directory: {solution_img_dir}"
                        )

                    # Make sure all subdirectories from images are created
                    for img_ref in image_refs:
                        # Get the directory part of the image path
                        img_dir = os.path.dirname(os.path.join(self.repo_path, img_ref))
                        if not os.path.exists(img_dir):
                            os.makedirs(img_dir, exist_ok=True)
                            logger.info(
                                f"Created directory for translated content: {img_dir}"
                            )

            return True

        except Exception as e:
            logger.error(f"Error ensuring images for translations: {str(e)}")
            return False
