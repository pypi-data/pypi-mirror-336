import typing

from .._types import IO

__all__ = ["AlreadyLocked", "FileToLarge", "LockException"]


class _BaseLockException(Exception):  # noqa: N818
    LOCK_FAILED = 1

    def __init__(
        self,
        *args: typing.Any,
        fh: IO | None | int = None,
        **kwargs: typing.Any,
    ) -> None:
        self.fh = fh
        Exception.__init__(self, *args)


class LockException(_BaseLockException):
    """Generic locking exception."""


class AlreadyLocked(LockException):
    """Exception thrown when the file is already locked."""


class FileToLarge(LockException):
    """Exception thrown when the file is too large to lock."""
