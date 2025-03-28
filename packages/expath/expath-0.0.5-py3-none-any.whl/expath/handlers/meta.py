import importlib.metadata
import importlib.resources
import pathlib
import shutil
import tempfile
import typing
from pathlib import Path as _PathlibPath
from urllib.parse import urlparse

from expath.handlers import PathHandler


class EntryPointsPathHandler(PathHandler):  # pragma: no cover
    """PathHandler that uses a package's metadata (entry point) to get the path."""

    def __init__(
        self,
        group: str,
        *,
        prefix: str | None = None,
        **kwargs,
    ):
        """
        Parameters
        ----------
        group : str
            The name of the entry point group to use.
        prefix : str
            The prefix to use for this path handler.
        trusted : bool
            Whether to trust the entry point group. If False, the entry point can only
            point to files in the package's data directory. If True, the entry point
            can specify code to be imported and ran.
        data : bool
            Whether to look for files in the package's data files.
        """
        super().__init__(**kwargs)

        if prefix is None:
            prefix = group + "://"

        self._tmp = tempfile.TemporaryDirectory()

        self.group = group
        self.prefix = prefix
        self.local = self._tmp.name

    def __del__(self):
        if self._tmp is not None:
            self._tmp.cleanup()

    @property
    @typing.override
    def _prefixes(self) -> tuple[str]:
        return (self.prefix,)

    @typing.override
    def _locate(self, path: str, **kwargs) -> _PathlibPath:
        with importlib.resources.as_file(self._get_traversable(path)) as ph:
            if not ph.is_file():
                msg = f"File {path!r} is not a file! Got: {ph!r}"
                raise FileNotFoundError(msg)
            local_path = _PathlibPath(self.local) / path[len(self.prefix) :]
            local_path.parent.mkdir(parents=True, exist_ok=True)
            if local_path.exists():
                local_path.unlink()
            shutil.copy(ph, local_path)
        return local_path

    def _get_traversable(self, path: str, **kwargs) -> _PathlibPath:
        url = urlparse(path)
        assert url.scheme == self.prefix.rstrip("://"), (  # noqa: B005
            f"Unsupported scheme {url.scheme!r}"
        )
        pkg_available = importlib.metadata.entry_points(group=self.group)
        pkg_req = url.netloc

        for pkg in pkg_available:
            if pkg.name == pkg_req:
                break
        else:
            msg = (
                f"Package {pkg_req!r} not found in group {self.group!r}. "
                f"Available packages: {pkg_available}"
            )
            raise ValueError(msg)

        # Check if the entrypoint is a callable
        if ":" in pkg.value:
            pkg, fn = pkg.value.split(":", 1)

            mod = importlib.import_module(pkg)
            return getattr(mod, fn)(url.path.lstrip("/"))

        # Otherwise, it is a path inside the package's data manifest
        pkg_files = importlib.resources.files(pkg.value)
        return pkg_files.joinpath(url.path.lstrip("/"))

    @typing.override
    def _isfile(self, path: str, **kwargs: typing.Any) -> bool:
        try:
            return self._locate(path, **kwargs).is_file()
        except FileNotFoundError:
            return False

    @typing.override
    def _isdir(self, path: str, **kwargs: typing.Any) -> bool:
        try:
            return self._locate(path, **kwargs).is_dir()
        except FileNotFoundError:
            return False

    @typing.override
    def _ls(self, path: str, **kwargs: typing.Any) -> list[str]:
        msg = f"Listing directories is not supported for {self.__class__.__name__}"
        raise NotImplementedError(msg)

    @typing.override
    def _open(self, path: str, mode="r", **kwargs):
        assert "w" not in mode, (
            f"Mode {mode!r} not supported for {self.__class__.__name__}"
        )
        return self._get_traversable(path).open(mode, **kwargs)


class PackageDataPathHandler(PathHandler):  # pragma: no cover
    """PathHandler that uses a distribution's manifest files to get the path."""

    def __init__(self, name: str, *, prefix: str | None = None, **kwargs):
        """
        Parameters
        ----------
        name : str
            The name of the distribution package to look for files in.
        prefix : str
            The prefix to use for this path handler.
        """
        super().__init__(**kwargs)

        if prefix is None:
            prefix = name + "://"

        self._tmp = tempfile.TemporaryDirectory()

        self.name = name
        self.prefix = prefix
        self.local = self._tmp.name

    def __del__(self):
        if self._tmp is not None:
            self._tmp.cleanup()

    @property
    @typing.override
    def _prefixes(self) -> tuple[str]:
        return (self.prefix,)

    @typing.override
    def _locate(self, path: str, **kwargs) -> pathlib.Path:
        files = importlib.resources.files(self.name)
        if files is None:
            msg = f"Package {self.name} not found"
            raise FileNotFoundError(msg)
        match = pathlib.PurePath(path[len(self.prefix) :])
        result = next((p for p in files if p == match), None)
        if result is None:
            msg = f"File {path!r} not found in package {self.name}"
            raise FileNotFoundError(msg)
        return result.locate()

    @typing.override
    def _isfile(self, path: str, **kwargs: typing.Any) -> bool:
        try:
            return self._locate(path, **kwargs).is_file()
        except FileNotFoundError:
            return False

    @typing.override
    def _isdir(self, path: str, **kwargs: typing.Any) -> bool:
        return False

    @typing.override
    def _ls(self, path: str, **kwargs: typing.Any) -> list[str]:
        msg = f"Listing directories is not supported for {self.__class__.__name__}"
        raise NotImplementedError(msg)

    @typing.override
    def _open(self, path: str, mode="r", **kwargs):
        assert "w" not in mode, (
            f"Mode {mode!r} not supported for {self.__class__.__name__}"
        )
        return self._locate(path).open(mode, **kwargs)
