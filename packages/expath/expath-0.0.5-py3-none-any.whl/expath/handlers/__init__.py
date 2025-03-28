from ._base import *
from ._io import *
from ._os import *

__lazy__ = ("env", "http", "onedrive", "wandb", "meta")


def __getattr__(name):
    import importlib

    if name in __lazy__:
        return importlib.import_module(f".{name}", package=__name__)
    msg = f"module '{__name__}' has no attribute '{name}'"
    raise AttributeError(msg)
