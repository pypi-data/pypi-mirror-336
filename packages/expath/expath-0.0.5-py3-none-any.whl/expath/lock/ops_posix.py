r"""OS-specific file locking ops for POSIX."""

import errno
import fcntl
import typing

from ._exceptions import AlreadyLocked, LockException
from ._flags import LockFlags

_apply_lock = fcntl.flock  # alternative is fcntl.lockf


def lock(file: int | typing.IO[str] | typing.IO[bytes], flags: LockFlags) -> None:  # type: ignore[misc]
    r"""Lock a file."""
    if (flags & LockFlags.NON_BLOCKING) and not flags & (
        LockFlags.SHARED | LockFlags.EXCLUSIVE
    ):
        msg = "When locking in non-blocking mode the SHARED/EXCLUSIVE flag is required."
        raise RuntimeError(
            msg,
        )

    try:
        _apply_lock(file, flags)
    except OSError as exc_value:
        if exc_value.errno in (errno.EACCES, errno.EAGAIN):
            raise AlreadyLocked(
                exc_value,
                fh=file,
            ) from exc_value
        raise LockException(
            exc_value,
            fh=file,
        ) from exc_value
    except EOFError as exc_value:
        raise LockException(
            exc_value,
            fh=file,
        ) from exc_value


def unlock(file: typing.IO[str] | typing.IO[bytes]) -> None:
    """Unlock a file."""
    _apply_lock(file.fileno(), LockFlags.UNBLOCK)
