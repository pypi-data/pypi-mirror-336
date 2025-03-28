import logging
import os
import pathlib
import typing
from collections import OrderedDict
from collections.abc import Callable, MutableMapping
from importlib.metadata import entry_points
from io import IOBase
from typing import Any, overload

from . import handlers
from ._types import PathType


class PathManager:
    """A class to open or translate paths."""

    def __init__(self, **options) -> None:
        self._handlers: MutableMapping[str, handlers.PathHandler] = OrderedDict()
        self._native: handlers.PathHandler = handlers.OSPathHandler()
        self._cwd: str | None = None
        self._handlers_async: set[handlers.PathHandler] = set()

        logger = logging.getLogger(__name__)

        for plugin in entry_points(group="expath"):
            try:
                handler = plugin.load()(**options)
            except Exception:
                logger.warning(
                    "Failed to load plugin %s",
                    plugin.name,
                    exc_info=True,
                )
            else:
                if handler is None:
                    continue
                self.register_handler(handler, allow_override=False)

    def get_handler(self, path: PathType) -> handlers.PathHandler:
        """Find a handler for the provided path.

        Parameters
        ----------
        path : str or os.PathLike or pathlib.PurePath
            URI path to resource

        Returns
        -------
        handlers.PathHandler
            Handler for this path

        """
        if isinstance(path, pathlib.Path):
            return self._native  # already OS path, no need to check other handlers
        path = os.fspath(path)
        return next(
            (h for p, h in self._handlers.items() if path.startswith(p)),
            self._native,
        )

    @overload
    def open(
        self,
        path: PathType,
        mode: typing.Literal["rb", "wb", "ab", "xb", "r+b", "w+b", "a+b", "x+b"] = ...,
        buffering: int = ...,
        **kwargs: Any,
    ) -> typing.IO[bytes]: ...

    @overload
    def open(
        self,
        path: PathType,
        mode: typing.Literal[
            "r",
            "w",
            "a",
            "x",
            "r+",
            "w+",
            "a+",
            "x+",
            "rt",
            "wt",
        ] = ...,
        buffering: int = ...,
        **kwargs: Any,
    ) -> typing.IO[str]: ...

    def open(
        self,
        path: PathType,
        mode: str = "r",
        buffering: int = -1,
        **kwargs: Any,
    ) -> typing.IO[str] | typing.IO[bytes]:
        handler = self.get_handler(path)
        return handler._open(path, mode, buffering=buffering, **kwargs)  # type: ignore[union-attr]

    def opena(
        self,
        path: PathType,
        mode: str = "r",
        buffering: int = -1,
        callback_after_file_close: Callable[[None], None] | None = None,
        **kwargs: Any,
    ) -> IOBase:
        """Open a file asynchronously.

        Parameters
        ----------
        path : str

        mode : str

        buffering : int

        callback_after_file_close : Optional[Callable]
            Called after close, if in write mode
        path: str :

        mode: str :
             (Default value = "r")
        buffering: int :
             (Default value = -1)
        callback_after_file_close: Optional[Callable[[None] :

        None]] :
             (Default value = None)
        **kwargs: Any :


        Returns
        -------


        """
        if "w" in mode:
            kwargs["callback_after_file_close"] = callback_after_file_close
            kwargs["buffering"] = buffering
        non_blocking_io = self.get_handler(path)._opena(
            path,
            mode,
            **kwargs,
        )
        if "w" in mode:
            # Keep track of the path handlers where `opena` is used so that all of the
            # threads can be properly joined on `PathManager.join`.
            self._handlers_async.add(self.get_handler(path))
        return non_blocking_io

    def async_join(self, *paths: str, **kwargs: Any) -> bool:
        """Wait for asynchronous writes to finish.

        Parameters
        ----------
        *paths : str
            File paths to wait on
        *paths: str :

        **kwargs: Any :


        Returns
        -------


        """
        success = True
        if not paths:  # Join all.
            for handler in self._handlers_async:
                success = handler._async_join(**kwargs) and success
        else:  # Join specific paths.
            for path in paths:
                success = self.get_handler(path)._async_join(path, **kwargs) and success
        return success

    def async_close(self, **kwargs: Any) -> bool:
        """Close all asynchronous I
        O threads.

        Parameters
        ----------
        **kwargs: Any :


        Returns
        -------


        """
        success = self.async_join(**kwargs)
        for handler in self._handlers_async:
            success = handler._async_close(**kwargs) and success
        self._handlers_async.clear()
        return success

    def copy(
        self,
        src_path: PathType,
        dst_path: PathType,
        overwrite: bool = False,
        **kwargs: Any,
    ) -> bool:
        """Copy a file from source to destination.

        Parameters
        ----------
        src_path : str

        dst_path : str

        overwrite : bool

        src_path: str :

        dst_path: str :

        overwrite: bool :
             (Default value = False)
        **kwargs: Any :


        Returns
        -------


        """
        if self.get_handler(src_path) != self.get_handler(  # type: ignore[union-attr]
            dst_path,
        ):
            return self._copy_across_handlers(src_path, dst_path, overwrite, **kwargs)

        handler = self.get_handler(src_path)
        return handler._copy(src_path, dst_path, overwrite, **kwargs)

    def mv(self, src_path: PathType, dst_path: PathType, **kwargs: Any) -> bool:
        """Move a source path to a destination."""
        assert self.get_handler(  # type: ignore[union-attr]
            src_path,
        ) == self.get_handler(dst_path), (
            "Src and dest paths must be supported by the same path handler."
        )
        handler = self.get_handler(src_path)
        return handler._mv(src_path, dst_path, **kwargs)

    def locate(
        self,
        path: PathType,
        force: bool = False,
        **kwargs: Any,
    ) -> pathlib.Path:
        """Get a local file path.

        Parameters
        ----------
        path : str

        force : bool

        path: str :

        force: bool :
             (Default value = False)
        **kwargs: Any :


        Returns
        -------


        """
        path = os.fspath(path)
        handler = self.get_handler(path)  # type: ignore[union-attr]
        try:
            bret = handler._locate(path, force=force, **kwargs)
        except TypeError:
            bret = handler._locate(path, **kwargs)
        return pathlib.Path(bret)

    def copy_from_local(
        self,
        local_path: str | pathlib.Path,
        dst_path: PathType,
        overwrite: bool = False,
        **kwargs: Any,
    ) -> bool:
        """Copy a local file to a destination URI.

        Parameters
        ----------
        local_path : str | pathlib.Path
            The local file path to copy from.

        dst_path : str

        overwrite : bool

        local_path: str :

        dst_path: str :

        overwrite: bool :
             (Default value = False)
        **kwargs: Any :


        Returns
        -------


        """
        local_path = pathlib.Path(local_path)
        assert local_path.exists(), f"local_path = {local_path}"
        handler = self.get_handler(dst_path)

        return handler._copy_from_local(
            local_path=local_path,
            dst_path=dst_path,
            overwrite=overwrite,
            **kwargs,
        )

    def exists(self, path: PathType, **kwargs: Any) -> bool:
        """Check if a resource exists at the given URI.

        Parameters
        ----------
        path : str

        path: str :

        **kwargs: Any :


        Returns
        -------


        """
        handler = self.get_handler(path)
        return handler._exists(path, **kwargs)  # type: ignore[union-attr]

    def isfile(self, path: PathType, **kwargs: Any) -> bool:
        """Check if the resource at the given URI is a file.

        Parameters
        ----------
        path : str

        path: str :

        **kwargs: Any :


        Returns
        -------


        """
        handler = self.get_handler(path)
        return handler._isfile(path, **kwargs)  # type: ignore[union-attr]

    def isdir(self, path: PathType, **kwargs: Any) -> bool:
        """Check if the resource at the given URI is a directory."""
        handler = self.get_handler(path)
        return handler._isdir(path, **kwargs)  # type: ignore[union-attr]

    def ls(self, path: PathType, **kwargs: Any) -> list[str]:
        """List the contents of a directory."""
        return self.get_handler(path)._ls(path, **kwargs)

    def mkdirs(self, path: PathType, **kwargs: Any) -> None:
        """Create directories recursively."""
        handler = self.get_handler(path)
        return handler._mkdirs(path, **kwargs)  # type: ignore[union-attr]

    def rm(self, path: PathType, **kwargs: Any) -> None:
        """Remove a file."""
        handler = self.get_handler(path)
        return handler._rm(path, **kwargs)  # type: ignore[union-attr]

    def symlink(self, src_path: PathType, dst_path: PathType, **kwargs: Any) -> bool:
        """Create a symlink from src_path to dst_path."""
        # Copying across handlers is not supported.
        assert self.get_handler(  # type: ignore[union-attr]
            src_path,
        ) == self.get_handler(dst_path)
        handler = self.get_handler(src_path)
        return handler._symlink(src_path, dst_path, **kwargs)  # type: ignore[union-attr]

    def set_cwd(self, path: str | None, **kwargs: Any) -> bool:
        """Set the current working directory."""
        if path is None and self._cwd is None:
            return True
        if self.get_handler(path or self._cwd)._set_cwd(path, **kwargs):  # type: ignore[union-attr]
            self._cwd = path
            bret = True
        else:
            bret = False
        return bret

    def register_handler(
        self,
        handler: handlers.PathHandler,
        allow_override: bool = True,
    ) -> None:
        """Register a path handler."""
        logging.getLogger(__name__)
        assert isinstance(handler, handlers.PathHandler), handler

        # Allow override of `OSPathHandler` which is automatically
        # instantiated by `PathManager`.
        if isinstance(handler, handlers.OSPathHandler):
            if allow_override:
                self._native = handler
            else:
                msg = (
                    "`OSPathHandler` is registered by default. Use the "
                    "`allow_override=True` kwarg to override it."
                )
                raise ValueError(msg)
            return

        for prefix in handler._prefixes:
            if prefix not in self._handlers:
                self._handlers[prefix] = handler
                continue

            old_handler_type = type(self._handlers[prefix])
            if allow_override:
                self._handlers[prefix] = handler
            else:
                msg = f"Prefix '{prefix}' already registered by {old_handler_type}!"
                raise KeyError(msg)

        # Sort path handlers in reverse order so longer prefixes take priority,
        # eg: http://foo/bar before http://foo
        self._handlers = OrderedDict(
            sorted(self._handlers.items(), key=lambda t: t[0], reverse=True),
        )

    def set_strict_kwargsing(self, enable: bool) -> None:
        """Toggle strict kwargs checking."""
        self._native._strict_kwargs = enable
        for handler in self._handlers.values():
            handler._strict_kwargs = enable

    def _copy_across_handlers(
        self,
        src_path: PathType,
        dst_path: PathType,
        overwrite: bool,
        **kwargs: Any,
    ) -> bool:
        src_handler = self.get_handler(src_path)
        assert src_handler._locate is not None
        dst_handler = self.get_handler(dst_path)
        assert dst_handler._copy_from_local is not None

        local_file = src_handler._locate(src_path, **kwargs)

        return dst_handler._copy_from_local(
            local_file,
            dst_path,
            overwrite=overwrite,
            **kwargs,
        )
