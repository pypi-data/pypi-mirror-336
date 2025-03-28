import base64
import typing
import logging
import os
from typing import Any

from .http import HTTPHandler


class OneDriveHandler(HTTPHandler):
    """Handler for OneDrive URLs.

    Notes
    -----
    Maps the short link to a direct download link.

    """

    ONE_DRIVE_PREFIX = "https://1drv.ms/u/s!"

    def create_one_drive_direct_download(self, one_drive_url: str) -> str:
        """Convert a short OneDrive URL into a direct download link.

        Parameters
        ----------
        one_drive_url : str
            The short OneDrive URL

        Returns
        -------
        str
            Direct download link

        """
        data_b64 = base64.b64encode(bytes(one_drive_url, "utf-8"))
        data_b64_string = (
            data_b64.decode("utf-8").replace("/", "_").replace("+", "-").rstrip("=")
        )
        return f"https://api.onedrive.com/v1.0/shares/u!{data_b64_string}/root/content"

    @property
    @typing.override
    def _prefixes(self) -> tuple[str, ...]:
        return (self.ONE_DRIVE_PREFIX,)

    #  inconsistently.
    def _locate(self, path: str, force: bool = False, **kwargs: Any) -> str:
        """This implementation downloads the remote resource and caches it locally.
        The resource will only be downloaded if not previously requested.
        """
        logger = logging.getLogger(__name__)
        direct_url = self.create_one_drive_direct_download(path)

        logger.info(f"URL {path} mapped to direct download link {direct_url}")

        return super()._locate(os.fspath(direct_url), force=force, **kwargs)
