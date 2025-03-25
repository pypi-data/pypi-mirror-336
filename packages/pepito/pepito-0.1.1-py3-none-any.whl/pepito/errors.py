class PepitoException(Exception):
    """
    Custom exception class, parent of all exceptions raised in Pepito
    """

    def __init__(self, message: str, error_code: int) -> None:
        super().__init__(message)
        self.error_code = error_code


class GitError(Exception):
    """
    Raised when a git command fails
    """

    def __init__(self, message: str) -> None:
        super().__init__(message, 1)


class CommitNotFound(PepitoException):
    """
    Raised when a commit is not found
    """

    def __init__(self, message: str) -> None:
        super().__init__(message, 2)


class NoDiffFound(Exception):
    """
    Raised when no diff is found between 2 files
    """

    def __init__(self, message: str) -> None:
        super().__init__(message, 3)


class NotAFile(Exception):
    """
    Raised when the provided file is not a file
    """

    def __init__(self, message: str) -> None:
        super().__init__(message, 4)


class InvalidChoice(Exception):
    """
    Raised when the user makes an invalid choice
    """

    def __init__(self, message: str) -> None:
        super().__init__(message, 5)


class InvalidHeader(Exception):
    """
    Raised when a header is invalid
    """

    def __init__(self, message: str) -> None:
        super().__init__(message, 6)
