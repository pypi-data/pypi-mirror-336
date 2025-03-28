r"""OS-specific file locking ops."""

# pragma: no cover

import os

if os.name == "nt":
    from .ops_win32 import lock, unlock
elif os.name == "posix":  # pragma: no cover
    from .ops_posix import lock, unlock
else:  # pragma: no cover
    msg = "Unsupported OS: {os.name}"
    raise RuntimeError(msg)

__all__ = ["lock", "unlock"]
