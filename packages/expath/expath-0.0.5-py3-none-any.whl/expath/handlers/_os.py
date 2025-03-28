import concurrent.futures
import errno
import logging
import os
import pathlib
import shutil
from collections.abc import Callable
from typing import IO, Any

from expath._types import PathType

from ._base import PathHandler

__all__ = ["OSPathHandler"]


class OSPathHandler(PathHandler):
    """Handles paths through the operating system."""

    _cwd = None

    def __init__(
        self,
        async_executor: concurrent.futures.Executor | None = None,
    ) -> None:
        super().__init__(async_executor)

    @property
    def _prefixes(self) -> tuple[str, ...]:
        return ()

    def _locate(
        self,
        path: PathType,
        force: bool = False,
        **kwargs: Any,
    ) -> pathlib.Path:
        self._check_kwargs(kwargs)
        return pathlib.Path(path)

    def _copy_from_local(
        self,
        local_path: PathType,
        dst_path: PathType,
        overwrite: bool = False,
        **kwargs: Any,
    ) -> None:
        self._check_kwargs(kwargs)
        local_path = self._get_path_with_cwd(local_path)
        dst_path = self._get_path_with_cwd(dst_path)
        assert self._copy(
            src_path=local_path,
            dst_path=dst_path,
            overwrite=overwrite,
            **kwargs,
        )

    def _open(
        self,
        path: PathType,
        mode: str = "r",
        buffering: int = -1,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        closefd: bool = True,
        opener: Callable | None = None,
        **kwargs: Any,
    ) -> IO[str] | IO[bytes]:
        r"""Open a path.

        Args:
            path (str): A URI supported by this PathHandler
            mode (str): Specifies the mode in which the file is opened. It defaults
                to 'r'.
            buffering (int): An optional integer used to set the buffering policy.
                Pass 0 to switch buffering off and an integer >= 1 to indicate the
                size in bytes of a fixed-size chunk buffer. When no buffering
                argument is given, the default buffering policy works as follows:
                    * Binary files are buffered in fixed-size chunks; the size of
                    the buffer is chosen using a heuristic trying to determine the
                    underlying device’s “block size” and falling back on
                    io.DEFAULT_BUFFER_SIZE. On many systems, the buffer will
                    typically be 4096 or 8192 bytes long.
            encoding (Optional[str]): the name of the encoding used to decode or
                encode the file. This should only be used in text mode.
            errors (Optional[str]): an optional string that specifies how encoding
                and decoding errors are to be handled. This cannot be used in binary
                mode.
            newline (Optional[str]): controls how universal newlines mode works
                (it only applies to text mode). It can be None, '', '\n', '\r',
                and '\r\n'.
            closefd (bool): If closefd is False and a file descriptor rather than
                a filename was given, the underlying file descriptor will be kept
                open when the file is closed. If a filename is given closefd must
                be True (the default) otherwise an error will be raised.
            opener (Optional[Callable]): A custom opener can be used by passing
                a callable as opener. The underlying file descriptor for the file
                object is then obtained by calling opener with (file, flags).
                opener must return an open file descriptor (passing os.open as opener
                results in functionality similar to passing None).

            See https://docs.python.org/3/library/functions.html#open for details.

        Returns:
            file: a file-like object.

        """
        self._check_kwargs(kwargs)
        return open(  # type: ignore
            self._get_path_with_cwd(path),
            mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
            closefd=closefd,
            opener=opener,
        )

    def _copy(
        self,
        src_path: PathType,
        dst_path: PathType,
        overwrite: bool = False,
        **kwargs: Any,
    ) -> bool:
        """Copies a source path to a destination path.

        Args:
            src_path (str): A URI supported by this PathHandler
            dst_path (str): A URI supported by this PathHandler
            overwrite (bool): Bool flag for forcing overwrite of existing file

        Returns:
            status (bool): True on success

        """
        self._check_kwargs(kwargs)
        src_path = self._get_path_with_cwd(src_path)
        dst_path = self._get_path_with_cwd(dst_path)
        if os.path.exists(dst_path) and not overwrite:
            logger = logging.getLogger(__name__)
            logger.error(f"Destination file {dst_path} already exists.")
            return False

        try:
            shutil.copyfile(src_path, dst_path)
            return True
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(f"Error in file copy - {e!s}")
            return False

    def _mv(self, src_path: PathType, dst_path: PathType, **kwargs: Any) -> bool:
        """Moves (renames) a source path to a destination path.

        Args:
            src_path (str): A URI supported by this PathHandler
            dst_path (str): A URI supported by this PathHandler

        Returns:
            status (bool): True on success

        """
        self._check_kwargs(kwargs)
        src_path = self._get_path_with_cwd(src_path)
        dst_path = self._get_path_with_cwd(dst_path)
        if os.path.exists(dst_path):
            logger = logging.getLogger(__name__)
            logger.error(f"Destination file {dst_path} already exists.")
            return False

        try:
            shutil.move(src_path, dst_path)
            return True
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(f"Error in move operation - {e!s}")
            return False

    def _symlink(self, src_path: PathType, dst_path: PathType, **kwargs: Any) -> bool:
        """Creates a symlink to the src_path at the dst_path.

        Args:
            src_path (str): A URI supported by this PathHandler
            dst_path (str): A URI supported by this PathHandler

        Returns:
            status (bool): True on success

        """
        self._check_kwargs(kwargs)
        src_path = self._get_path_with_cwd(src_path)
        dst_path = self._get_path_with_cwd(dst_path)
        logger = logging.getLogger(__name__)
        if not os.path.exists(src_path):
            logger.error(f"Source path {src_path} does not exist")
            return False
        if os.path.exists(dst_path):
            logger.error(f"Destination path {dst_path} already exists.")
            return False
        try:
            os.symlink(src_path, dst_path)
            return True
        except Exception as e:
            logger.exception(f"Error in symlink - {e!s}")
            return False

    def _exists(self, path: PathType, **kwargs: Any) -> bool:
        self._check_kwargs(kwargs)
        return os.path.exists(self._get_path_with_cwd(path))

    def _isfile(self, path: PathType, **kwargs: Any) -> bool:
        self._check_kwargs(kwargs)
        return os.path.isfile(self._get_path_with_cwd(path))

    def _isdir(self, path: PathType, **kwargs: Any) -> bool:
        self._check_kwargs(kwargs)
        return os.path.isdir(self._get_path_with_cwd(path))

    def _ls(self, path: PathType, **kwargs: Any) -> list[str]:
        self._check_kwargs(kwargs)
        return os.listdir(self._get_path_with_cwd(path))

    def _mkdirs(self, path: PathType, **kwargs: Any) -> None:
        self._check_kwargs(kwargs)
        try:
            os.makedirs(path, exist_ok=True)
        except OSError as e:
            # EEXIST it can still happen if multiple processes are creating the dir
            if e.errno != errno.EEXIST:
                raise

    def _rm(self, path: PathType, **kwargs: Any) -> None:
        self._check_kwargs(kwargs)
        os.remove(path)

    def _set_cwd(self, path: str | None, **kwargs: Any) -> bool:
        self._check_kwargs(kwargs)
        # Remove cwd path if None
        if path is None:
            self._cwd = None
            return True

        # Make sure path is a valid Unix path
        if not os.path.exists(path):
            msg = f"{path} is not a valid Unix path"
            raise ValueError(msg)
        # Make sure path is an absolute path
        if not os.path.isabs(path):
            msg = f"{path} is not an absolute path"
            raise ValueError(msg)
        self._cwd = path
        return True

    def _get_path_with_cwd(self, path: str) -> str:
        if not path:
            return path
        return os.path.normpath(
            path if not self._cwd else os.path.join(self._cwd, path),
        )
