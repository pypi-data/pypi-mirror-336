import logging
import os
import typing
from typing import IO, Any
from urllib.parse import urlparse

from .._download import download, ensure_cache
from ..lock import file_lock
from ._base import PathHandler


class HTTPHandler(PathHandler):
    """Download URLs and cache them to disk."""

    MAX_FILENAME_LEN = 250

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.cache_map: dict[str, str] = {}

    @property
    @typing.override
    def _prefixes(self) -> tuple[str, ...]:
        return ("http://", "https://", "ftp://")

    @typing.override
    def _locate(
        self,
        path: str,
        force: bool = False,
        cache_dir: str | None = None,
        **kwargs: Any,
    ) -> str:
        """This implementation downloads the remote resource and caches it locally.
        The resource will only be downloaded if not previously requested.
        """
        self._check_kwargs(kwargs)
        if (
            force
            or path not in self.cache_map
            or not os.path.exists(self.cache_map[path])
        ):
            logger = logging.getLogger(__name__)
            parsed_url = urlparse(path)
            dirname = os.path.join(
                ensure_cache(cache_dir),
                os.path.dirname(parsed_url.path.lstrip("/")),
            )
            filename = path.split("/")[-1]

            if parsed_url.query:
                filename = filename.split("?").pop(0)

            if len(filename) > self.MAX_FILENAME_LEN:
                filename = filename[:100] + "_" + uuid.uuid4().hex

            cached = os.path.join(dirname, filename)
            with file_lock(cached):
                if not os.path.isfile(cached):
                    logger.info(f"Downloading {path} ...")
                    cached = download(path, dirname, filename=filename)
            logger.info(f"URL {path} cached in {cached}")
            self.cache_map[path] = cached
        return self.cache_map[path]

    @typing.override
    def _open(
        self,
        path: str,
        mode: str = "r",
        buffering: int = -1,
        **kwargs: Any,
    ) -> IO[str] | IO[bytes]:
        """Open a remote HTTP path. The resource is first downloaded and cached
        locally.

        Args:
            path (str): A URI supported by this PathHandler
            mode (str): Specifies the mode in which the file is opened. It defaults
                to 'r'.
            buffering (int): Not used for this PathHandler.

        Returns:
            file: a file-like object.

        """
        self._check_kwargs(kwargs)
        assert mode in ("r", "rb"), (
            f"{self.__class__.__name__} does not support open with {mode} mode"
        )
        assert buffering == -1, (
            f"{self.__class__.__name__} does not support the `buffering` argument"
        )
        local_path = self._locate(path, force=False)
        return open(local_path, mode)
