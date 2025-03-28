import abc
import concurrent.futures
import logging
import pathlib
import typing
from collections.abc import Callable
from io import IOBase

from .._types import IO, PathType
from ._io import NonBlockingIOManager

__all__ = ["PathHandler"]


class PathHandler(metaclass=abc.ABCMeta):
    """
    Protocol class for path handlers.
    """

    _strict_kwargs = True

    def __init__(
        self,
        async_executor: concurrent.futures.Executor | None = None,
        **kwargs: typing.Any,
    ) -> None:
        """Initialize the PathHandler.

        When registering a `PathHandler`, the user can optionally pass in a
        `Executor` to run the asynchronous file operations.

        NOTE: For regular non-async operations of `PathManager`, there is
        no need to pass `async_executor`.

        Parameters
        ----------
        async_executor: concurrent.futures.Executor | None
            Used for async file operations.

        """
        super().__init__(**kwargs)

        self._non_blocking_io_manager = None
        self._non_blocking_io_executor = async_executor

    def _check_kwargs(self, kwargs: dict[str, typing.Any]) -> None:
        """Check whether arguments are empty.

        Throws a ValueError if strict
        kwargs checking is enabled and args are non-empty. If strict kwargs
        checking is disabled, only a warning is logged.

        Args:
            kwargs (dict[str, typing.Any])

        """
        if self._strict_kwargs:
            if len(kwargs) > 0:
                msg = f"Unused arguments: {kwargs}"
                raise ValueError(msg)
        else:
            logger = logging.getLogger(__name__)
            logger.warning(
                "unused arguments: %s",
                ", ".join(f"{k}={v}" for k, v in kwargs.items()),
                stacklevel=2,
            )

    @property
    @abc.abstractmethod
    def _prefixes(self) -> typing.Iterable[str]:
        """Get supported prefixes for this handler.

        Returns
        -------
        list[str]
            The list of URI prefixes this PathHandler can support

        """
        ...

    def _locate(
        self,
        path: PathType,
        force: bool = False,
        **kwargs: typing.Any,
    ) -> pathlib.Path:
        raise NotImplementedError()

    def _copy_from_local(
        self,
        local_path: PathType,
        dst_path: PathType,
        overwrite: bool = False,
        **kwargs: typing.Any,
    ) -> bool | None:
        """Copies a local file to the specified URI.

        If the URI is another local path, this should be functionally identical
        to copy.

        Args:
            local_path (str): a file path which exists on the local file system
            dst_path (str): A URI supported by this PathHandler
            overwrite (bool): Bool flag for forcing overwrite of existing URI

        Returns:
            status (bool): True on success

        """
        raise NotImplementedError()

    def _open(
        self,
        path: PathType,
        mode: str = "r",
        buffering: int = -1,
        **kwargs: typing.Any,
    ) -> IO:
        """Open a stream to a URI, similar to the built-in `open`.

        Args:
            path (str): A URI supported by this PathHandler
            mode (str): Specifies the mode in which the file is opened. It defaults
                to 'r'.
            buffering (int): An optional integer used to set the buffering policy.
                Pass 0 to switch buffering off and an integer >= 1 to indicate the
                size in bytes of a fixed-size chunk buffer. When no buffering
                argument is given, the default buffering policy depends on the
                underlying I/O implementation.

        Returns:
            file: a file-like object.

        """
        raise NotImplementedError()

    def _opena(
        self,
        path: PathType,
        mode: str = "r",
        callback_after_file_close: Callable[[None], None] | None = None,
        buffering: int = -1,
        **kwargs: typing.Any,
    ) -> IOBase:
        # Restrict mode until `NonBlockingIO` has async read feature.
        valid_modes = {"w", "a", "b"}
        if not all(m in valid_modes for m in mode):
            msg = f"`opena` mode must be write or append for path {path}"
            raise ValueError(msg)

        # TODO: Each `PathHandler` should set its own `self._buffered`
        # parameter and pass that in here. Until then, we assume no
        # buffering for any storage backend.
        if not self._non_blocking_io_manager:
            self._non_blocking_io_manager = NonBlockingIOManager(
                buffered=False,
                executor=self._non_blocking_io_executor,
            )

        try:
            return self._non_blocking_io_manager.get_non_blocking_io(
                path=self._get_path_with_cwd(path),
                io_obj=self._open(path, mode, **kwargs),
                callback_after_file_close=callback_after_file_close,
                buffering=buffering,
            )
        except ValueError:
            # When `_strict_kwargs = True`, then `open_callable`
            # will throw a `ValueError`. This generic `_opena` function
            # does not check the kwargs since it may include any `_open`
            # args like `encoding`, `ttl`, `has_user_data`, etc.
            logger = logging.getLogger(__name__)
            logger.exception(
                "An exception occurred in `NonBlockingIOManager`. This "
                "is most likely due to invalid `opena` args. Make sure "
                "they match the `open` args for the `PathHandler`.",
            )
            self._async_close()

    def _async_join(
        self,
        path: str | None = None,
        **kwargs: typing.Any,
    ) -> bool:
        """Ensures that desired async write threads are properly joined.

        Args:
            path (str): Pass in a file path to wait until all asynchronous
                activity for that path is complete. If no path is passed in,
                then this will wait until all asynchronous jobs are complete.

        Returns:
            status (bool): True on success

        """
        if not self._non_blocking_io_manager:
            logger = logging.getLogger(__name__)
            logger.warning(
                "This is an async feature. No threads to join because "
                "`opena` was not used.",
            )
        self._check_kwargs(kwargs)
        return self._non_blocking_io_manager._join(
            self._get_path_with_cwd(path) if path else None,
        )

    def _async_close(self, **kwargs: typing.Any) -> bool:
        """Closes the thread pool used for the asynchronous operations.

        Returns:
            status (bool): True on success

        """
        if not self._non_blocking_io_manager:
            logger = logging.getLogger(__name__)
            logger.warning(
                "This is an async feature. No threadpool to close because "
                "`opena` was not used.",
            )
        self._check_kwargs(kwargs)
        return self._non_blocking_io_manager._close_thread_pool()

    def _copy(
        self,
        src_path: PathType,
        dst_path: PathType,
        overwrite: bool = False,
        **kwargs: typing.Any,
    ) -> bool:
        """Copies a source path to a destination path.

        Args:
            src_path (str): A URI supported by this PathHandler
            dst_path (str): A URI supported by this PathHandler
            overwrite (bool): Bool flag for forcing overwrite of existing file

        Returns:
            status (bool): True on success

        """
        raise NotImplementedError()

    def _mv(self, src_path: PathType, dst_path: PathType, **kwargs: typing.Any) -> bool:
        """Moves (renames) a source path to a destination path.

        Args:
            src_path (str): A URI supported by this PathHandler
            dst_path (str): A URI supported by this PathHandler

        Returns:
            status (bool): True on success

        """
        raise NotImplementedError()

    def _exists(self, path: PathType, **kwargs: typing.Any) -> bool:
        """Checks if there is a resource at the given URI.

        Args:
            path (str): A URI supported by this PathHandler

        Returns:
            bool: true if the path exists

        """
        raise NotImplementedError()

    def _isfile(self, path: PathType, **kwargs: typing.Any) -> bool:
        """Checks if the resource at the given URI is a file.

        Args:
            path (str): A URI supported by this PathHandler

        Returns:
            bool: true if the path is a file

        """
        raise NotImplementedError()

    def _isdir(self, path: PathType, **kwargs: typing.Any) -> bool:
        """Checks if the resource at the given URI is a directory.

        Args:
            path (str): A URI supported by this PathHandler

        Returns:
            bool: true if the path is a directory

        """
        raise NotImplementedError()

    def _ls(self, path: PathType, **kwargs: typing.Any) -> list[str]:
        """List the contents of the directory at the provided URI.

        Args:
            path (str): A URI supported by this PathHandler

        Returns:
            list[str]: list of contents in given path

        """
        raise NotImplementedError()

    def _mkdirs(self, path: PathType, **kwargs: typing.Any) -> None:
        """Recursive directory creation function. Like mkdir(), but makes all
        intermediate-level directories needed to contain the leaf directory.
        Similar to the native `os.makedirs`.

        Args:
            path (str): A URI supported by this PathHandler

        """
        raise NotImplementedError()

    def _rm(self, path: PathType, **kwargs: typing.Any) -> None:
        """Remove the file (not directory) at the provided URI.

        Args:
            path (str): A URI supported by this PathHandler

        """
        raise NotImplementedError()

    def _symlink(
        self,
        src_path: PathType,
        dst_path: PathType,
        **kwargs: typing.Any,
    ) -> bool:
        """Symlink the src_path to the dst_path.

        Args:
            src_path (str): A URI supported by this PathHandler to symlink from
            dst_path (str): A URI supported by this PathHandler to symlink to

        """
        raise NotImplementedError()

    def _set_cwd(self, path: str | None, **kwargs: typing.Any) -> bool:
        """Set the current working directory. PathHandler classes prepend the cwd
        to all URI paths that are handled.

        Args:
            path (str) or None: A URI supported by this PathHandler. Must be a valid
                absolute path or None to set the cwd to None.

        Returns:
            bool: true if cwd was set without errors

        """
        raise NotImplementedError()

    def _get_path_with_cwd(self, path: str) -> str:
        """Default implementation. PathHandler classes that provide a `_set_cwd`
        feature should also override this `_get_path_with_cwd` method.

        Args:
            path (str): A URI supported by this PathHandler.

        Returns:
            path (str): Full path with the cwd attached.

        """
        return path
