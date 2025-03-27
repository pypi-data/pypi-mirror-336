from typing import List, Optional, Union

from darca_exception.exception import DarcaException
from darca_executor import DarcaExecError, DarcaExecutor
from darca_log_facility.logger import DarcaLogger

logger = DarcaLogger(name="darca-git").get_logger()


class GitException(DarcaException):
    """
    Exception raised for any failure in Git operations.
    Provides error_code, metadata, and optional cause exception
    for traceability.
    """

    def __init__(self, message, error_code=None, metadata=None, cause=None):
        super().__init__(
            message=message,
            error_code=error_code or "GIT_ERROR",
            metadata=metadata,
            cause=cause,
        )


class Git:
    """
    Core Git interface that delegates Git CLI calls through the secure
    DarcaExecutor.
    This class provides Git operations without depending on external
    Git libraries.
    """

    def __init__(self):
        self.executor = DarcaExecutor(use_shell=False)

    def _run(self, args: List[str], cwd: str, error_code: str) -> str:
        """
        Internal helper to run a Git command via the executor.

        Args:
            args: Git CLI arguments (excluding 'git' itself)
            cwd: Working directory to run the command in
            error_code: Error code for structured exception

        Returns:
            stdout from the Git command

        Raises:
            GitException on failure
        """
        try:
            logger.debug(
                f"Running git command: git {' '.join(args)} in '{cwd}'"
            )
            result = self.executor.run(["git"] + args, cwd=cwd)
            return result.stdout
        except DarcaExecError as e:
            logger.error(
                f"Git command failed: git {' '.join(args)} in '{cwd}'"
            )
            raise GitException(
                message="Git command failed.",
                error_code=error_code,
                metadata={"args": args, "cwd": cwd},
                cause=e,
            )

    def _checkout(self, args: List[str], cwd: str, error_code: str) -> None:
        """
        Internal helper for all Git checkout operations.

        Args:
            args: Git checkout arguments
            cwd: Repo path
            error_code: Associated error code for exceptions
        """
        self._run(["checkout"] + args, cwd, error_code=error_code)

    def init(self, cwd: str) -> None:
        """
        Initialize a Git repository in the given directory.

        Args:
            cwd: Directory path to initialize repo in
        """
        logger.info(f"Initializing git repository in '{cwd}'")
        self._run(["init"], cwd, error_code="GIT_INIT_FAILED")

    def clone(self, repo_url: str, cwd: str) -> None:
        """
        Clone a Git repository into the given directory.

        Args:
            repo_url: The Git repository URL
            cwd: Destination path
        """
        logger.info(f"Cloning repository '{repo_url}' into '{cwd}'")
        self._run(["clone", repo_url, "."], cwd, error_code="GIT_CLONE_FAILED")

    def status(self, cwd: str, porcelain: bool = True) -> str:
        """
        Get repository status (optionally in porcelain format).

        Args:
            cwd: Path to the repository
            porcelain: Whether to use --porcelain (machine-readable)

        Returns:
            Git status output as string
        """
        args = ["status", "--porcelain"] if porcelain else ["status"]
        logger.debug(f"Getting git status (porcelain={porcelain}) in '{cwd}'")
        return self._run(args, cwd, error_code="GIT_STATUS_FAILED")

    def add(self, path: str, cwd: str) -> None:
        """
        Stage a file or path for commit.

        Args:
            path: Path to add (relative or absolute)
            cwd: Path to the repository
        """
        logger.debug(f"Adding file '{path}' in '{cwd}'")
        self._run(["add", path], cwd, error_code="GIT_ADD_FAILED")

    def commit(self, message: str, cwd: str) -> None:
        """
        Commit staged changes with a message.

        Args:
            message: Commit message
            cwd: Path to the repository
        """
        logger.info(f"Committing changes in '{cwd}' with message: {message}")
        self._run(
            ["commit", "-m", message], cwd, error_code="GIT_COMMIT_FAILED"
        )

    def pull(self, cwd: str) -> None:
        """
        Pull the latest changes from the current branch's remote.

        Args:
            cwd: Path to the repository
        """
        logger.info(f"Pulling latest changes in '{cwd}'")
        self._run(["pull"], cwd, error_code="GIT_PULL_FAILED")

    def push(self, cwd: str, remote_url: Optional[str] = None) -> None:
        """
        Push local changes to the remote repository.

        Args:
            cwd: Path to the repository
            remote_url: Optional override for the 'origin' remote URL
        """
        logger.info(f"Pushing changes from '{cwd}'")
        if remote_url:
            logger.info(f"Setting remote 'origin' to '{remote_url}'")
            self._run(
                ["remote", "remove", "origin"],
                cwd,
                error_code="GIT_REMOTE_REMOVE_FAILED",
            )
            self._run(
                ["remote", "add", "origin", remote_url],
                cwd,
                error_code="GIT_REMOTE_ADD_FAILED",
            )
        self._run(
            ["push", "-u", "origin", "HEAD"], cwd, error_code="GIT_PUSH_FAILED"
        )

    def checkout_branch(
        self, cwd: str, branch: str, create: bool = False
    ) -> None:
        """
        Switch to a branch (optionally creating it first).

        Args:
            cwd: Path to the repository
            branch: Branch name
            create: Whether to create the branch before switching
        """
        logger.info(
            f"{'Creating and checking out' if create else 'Checking out'} "
            f"branch '{branch}' in '{cwd}'"
        )
        args = ["-b", branch] if create else [branch]
        self._checkout(args, cwd, error_code="GIT_CHECKOUT_BRANCH_FAILED")

    def checkout_path(self, cwd: str, paths: Union[str, List[str]]) -> None:
        """
        Revert uncommitted changes in one or more paths.

        Args:
            cwd: Path to the repository
            paths: Single path or list of paths to restore
        """
        if isinstance(paths, str):
            paths = [paths]
        logger.info(
            f"Reverting local changes to: {', '.join(paths)} in '{cwd}'"
        )
        self._checkout(
            ["--"] + paths, cwd, error_code="GIT_CHECKOUT_PATH_FAILED"
        )

    def checkout_path_from_branch(
        self, cwd: str, branch: str, paths: Union[str, List[str]]
    ) -> None:
        """
        Restore file(s) from a specific branch without switching branches.

        Args:
            cwd: Path to the repository
            branch: Source branch to checkout from
            paths: Path(s) to restore from the branch
        """
        if isinstance(paths, str):
            paths = [paths]
        logger.info(
            f"Restoring files {', '.join(paths)} from branch '{branch}'"
            f" in '{cwd}'"
        )
        self._checkout(
            [branch, "--"] + paths,
            cwd,
            error_code="GIT_CHECKOUT_PATH_FROM_BRANCH_FAILED",
        )
