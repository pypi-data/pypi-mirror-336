import os
import pathlib
import tempfile
import typing

from ._base import PathHandler


class EnvironPathHandler(PathHandler):
    """PathHandler that uses an environment variable to get the path.

    Parameters
    ----------
    prefix : str
        The prefix to use for this path handler.
    env : str
        The name of the environment variable to use.
    default : str | None, optional
        The default value to use if the environment variable is not defined, by default None.
        If None is passed, then a temporary directory is created.

    Raises
    ------
    ValueError
        If the environment variable is not defined and no default is provided.

    Examples
    --------
    >>> import os
    >>> os.environ["DATASETS"] = "/datasets"
    >>> handler = EnvPathHandler("//datasets/", "DATASETS")
    >>> handler.locate("//datasets/foo/bar.txt")
    '/datasets/foo/bar.txt'

    """

    def __init__(self, prefix: str, *env: str, default: str | None = None, **kwargs):
        super().__init__(**kwargs)

        self._tmp = None
        for env_key in env:
            value = os.getenv(env_key)
            if value is None or len(value) == 0 or value[0] == "-":
                continue
            break
        else:
            if default is None:
                self._tmp = tempfile.TemporaryDirectory()
                value = self._tmp.name
            else:
                value = default

        value = os.path.expanduser(value)
        value = os.path.realpath(value)

        self.PREFIX: typing.Final = prefix
        self.LOCAL: typing.Final = value

    @property
    @typing.override
    def _prefixes(self) -> tuple[str, ...]:
        """ """
        return (self.PREFIX,)

    def _get_path(self, path: str, **kwargs) -> pathlib.Path:
        """Parameters
        ----------
        path: str :

        **kwargs :


        Returns
        -------

        """
        name = path[len(self.PREFIX) :]
        if len(name) == 0:
            return pathlib.Path(self.LOCAL).resolve()
        return pathlib.Path(self.LOCAL, *name.split("/")).resolve()

    @typing.override
    def _locate(self, path: str, **kwargs):
        """Parameters
        ----------
        path: str :

        **kwargs :


        Returns
        -------

        """
        return str(self._get_path(path, **kwargs))

    @typing.override
    def _isfile(self, path: str, **kwargs: typing.Any) -> bool:
        """Parameters
        ----------
        path: str :

        **kwargs: typing.Any :


        Returns
        -------

        """
        return self._get_path(path, **kwargs).is_file()

    @typing.override
    def _isdir(self, path: str, **kwargs: typing.Any) -> bool:
        """Parameters
        ----------
        path: str :

        **kwargs: typing.Any :


        Returns
        -------

        """
        return self._get_path(path, **kwargs).is_dir()

    @typing.override
    def _ls(self, path: str, **kwargs: typing.Any) -> list[str]:
        """Parameters
        ----------
        path: str :

        **kwargs: typing.Any :


        Returns
        -------

        """
        return sorted(p.name for p in self._get_path(path, **kwargs).iterdir())

    @typing.override
    def _open(self, path: str, mode="r", **kwargs):
        """Parameters
        ----------
        path: str :

        mode :
             (Default value = "r")
        **kwargs :


        Returns
        -------

        """
        # name = path[len(self.PREFIX) :]
        # return _g_manager.open(self.LOCAL + name, mode, **kwargs)
        return open(self._locate(path), mode, **kwargs)

    def __del__(self):
        if self._tmp is not None:
            self._tmp.cleanup()
