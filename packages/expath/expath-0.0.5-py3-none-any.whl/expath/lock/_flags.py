"""Locking constants and flags."""

import enum
import os

__all__ = ["LOCK_EX", "LOCK_NB", "LOCK_SH", "LOCK_UN", "LockFlags"]

if os.name == "nt":  # pragma: no cover
    import msvcrt

    _OS_EXCLUSIVE = 0x1
    _OS_SHARED = 0x2
    _OS_NON_BLOCKING = 0x4
    _OS_UNLOCK = msvcrt.LK_UNLCK  # type: ignore[attr-defined]

elif os.name == "posix":  # pragma: no cover
    import fcntl

    _OS_EXCLUSIVE = fcntl.LOCK_EX
    _OS_SHARED = fcntl.LOCK_SH
    _OS_NON_BLOCKING = fcntl.LOCK_NB
    _OS_UNLOCK = fcntl.LOCK_UN

else:  # pragma: no cover
    msg = f"Unsupported OS: {os.name}"
    raise RuntimeError(msg)


class LockFlags(enum.IntFlag):
    r"""Enumeration of lock flags. The values are OS-specific."""

    EXCLUSIVE = _OS_EXCLUSIVE
    SHARED = _OS_SHARED
    NON_BLOCKING = _OS_NON_BLOCKING
    UNBLOCK = _OS_UNLOCK


# Constants for the lock flags following `fcntl` convention
LOCK_EX = LockFlags.EXCLUSIVE
LOCK_SH = LockFlags.SHARED
LOCK_NB = LockFlags.NON_BLOCKING
LOCK_UN = LockFlags.UNBLOCK
