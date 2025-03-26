"""custom exceptions for dumb-datasets."""


class DumbDatasetsException(Exception):
    """base exception for dumb-datasets users."""

    pass


class IntermediateDataError(DumbDatasetsException):
    """error related to intermediate data operations."""

    pass


class MetadataNotFoundError(IntermediateDataError):
    """error when metadata file is not found."""

    def __init__(self, message: str = "metadata not found") -> None:
        super().__init__(message)


class FileAlreadyExistsError(IntermediateDataError):
    """error when file already exists in the repository."""

    def __init__(self, path: str = "") -> None:
        message = f"file exists: {path}"
        super().__init__(message)


class BranchCreationError(IntermediateDataError):
    """error when creating a branch fails."""

    def __init__(self, message: str = "branch creation failed") -> None:
        super().__init__(message)


class DownloadError(IntermediateDataError):
    """error when downloading files fails."""

    def __init__(self, message: str = "download failed", repo_id: str = "", branch: str = "") -> None:
        if repo_id and branch:
            message = f"download failed for {repo_id}/{branch}: {message}"
        elif repo_id:
            message = f"download failed for {repo_id}: {message}"
        super().__init__(message)


class FileUploadError(IntermediateDataError):
    """error when uploading files fails."""

    def __init__(self, path: str = "", repo_id: str = "", branch: str = "") -> None:
        message = "upload failed"
        if repo_id and branch and path:
            message = f"failed to upload {path} to {repo_id}/{branch}"
        elif repo_id and path:
            message = f"failed to upload {path} to {repo_id}"
        super().__init__(message)


class DataFileNotFoundError(IntermediateDataError):
    """error when a file is not found."""

    def __init__(self, path: str = "") -> None:
        message = f"file not found: {path}"
        super().__init__(message)


class ProcessingLogError(IntermediateDataError):
    """error for logging processing actions."""

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class UploadedFileError(IntermediateDataError):
    """error related to uploaded files."""

    def __init__(self, file_name: str = "", path: str = "") -> None:
        message = f"uploaded {file_name} to {path}"
        super().__init__(message)
