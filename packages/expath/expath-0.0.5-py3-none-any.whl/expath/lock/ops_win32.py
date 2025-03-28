r"""OS-specific file locking ops for Windows."""

# pragma: no cover

import enum
import msvcrt
import typing

import pywintypes
import win32con
import win32file
import winerror

from ._exceptions import AlreadyLocked, LockException


class LockFlags(enum.IntFlag):
    """Lock flag constants for file locking."""

    EXCLUSIVE = 0x1
    SHARED = 0x2
    NON_BLOCKING = 0x4
    UNBLOCK = msvcrt.LK_UNLCK


OVERLAPPED = pywintypes.OVERLAPPED()


def lock(file: int | typing.IO[str] | typing.IO[bytes], flags: LockFlags) -> None:  # type: ignore[misc]
    file = typing.cast(typing.IO[bytes] | typing.IO[str], file)
    mode = 0
    if flags & LockFlags.NON_BLOCKING:
        mode |= win32con.LOCKFILE_FAIL_IMMEDIATELY
    if flags & LockFlags.EXCLUSIVE:
        mode |= win32con.LOCKFILE_EXCLUSIVE_LOCK

    savepos = file.tell()
    if savepos:
        file.seek(0)

    os_fh = msvcrt.get_osfhandle(file.fileno())  # type: ignore[attr-defined]
    try:
        win32file.LockFileEx(os_fh, mode, 0, -0x10000, OVERLAPPED)
    except pywintypes.error as exc_value:
        if exc_value.winerror == winerror.ERROR_LOCK_VIOLATION:
            raise AlreadyLocked(
                LockException.LOCK_FAILED,
                exc_value.strerror,
                fh=file,
            ) from exc_value
        raise
    finally:
        if savepos:
            file.seek(savepos)


def unlock(file: typing.IO[str] | typing.IO[bytes]) -> None:
    try:
        savepos = file.tell()
        if savepos:
            file.seek(0)

        os_fh = msvcrt.get_osfhandle(file.fileno())  # type: ignore[attr-defined]
        try:
            win32file.UnlockFileEx(
                os_fh,
                0,
                -0x10000,
                OVERLAPPED,
            )
        except pywintypes.error as exc:
            if exc.winerror != winerror.ERROR_NOT_LOCKED:
                # Q:  Are there exceptions/codes we should be
                # dealing with here?
                raise
        finally:
            if savepos:
                file.seek(savepos)
    except OSError as exc:
        raise LockException(
            LockException.LOCK_FAILED,
            exc.strerror,
            fh=file,
        ) from exc
