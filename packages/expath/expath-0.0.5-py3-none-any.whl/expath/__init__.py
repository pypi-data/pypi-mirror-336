"""
Expath
======

This is the standalone version of the `unipercept.fileio` module. It was refactored
such that it can be installed independently of the `unipercept` package.

"""

from . import manager
from ._download import *
from ._types import *

# Declare the default path manager
DEFAULT_MANAGER: manager.PathManager = manager.PathManager()

# Redirect basic IO methods to the default manager. This is the default mode of
# interaction for most users.
async_close = DEFAULT_MANAGER.async_close
async_join = DEFAULT_MANAGER.async_join
copy = DEFAULT_MANAGER.copy
copy_from_local = DEFAULT_MANAGER.copy_from_local
exists = DEFAULT_MANAGER.exists
get_handler = DEFAULT_MANAGER.get_handler
locate = DEFAULT_MANAGER.locate
isdir = DEFAULT_MANAGER.isdir
isfile = DEFAULT_MANAGER.isfile
ls = DEFAULT_MANAGER.ls
mkdirs = DEFAULT_MANAGER.mkdirs
mv = DEFAULT_MANAGER.mv
open = DEFAULT_MANAGER.open
opena = DEFAULT_MANAGER.opena
rm = DEFAULT_MANAGER.rm
symlink = DEFAULT_MANAGER.symlink


# Version from installation metadata
__version__: str


def __getattr__(name: str):
    from importlib.metadata import PackageNotFoundError, version

    match name:
        case "__version__":
            try:
                return version(__name__)
            except PackageNotFoundError:
                return "unknown"
        case _:
            pass

    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)
