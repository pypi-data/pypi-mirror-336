import os
import pathlib
import typing

__all__ = ["IO", "FileOpenKwargs", "Mode", "PathType"]

type PathType = str | os.PathLike | pathlib.PurePath

# fmt: off
Mode = typing.Literal[
    # Text modes
    # Read text
    "r", "rt", "tr",
    # Write text
    "w", "wt", "tw",
    # Append text
    "a", "at", "ta",
    # Exclusive creation text
    "x", "xt", "tx",
    # Read and write text
    "r+", "+r", "rt+", "r+t", "+rt", "tr+", "t+r", "+tr",
    # Write and read text
    "w+", "+w", "wt+", "w+t", "+wt", "tw+", "t+w", "+tw",
    # Append and read text
    "a+", "+a", "at+", "a+t", "+at", "ta+", "t+a", "+ta",
    # Exclusive creation and read text
    "x+", "+x", "xt+", "x+t", "+xt", "tx+", "t+x", "+tx",
    # Universal newline support
    "U", "rU", "Ur", "rtU", "rUt", "Urt", "trU", "tUr", "Utr",

    # Binary modes
    # Read binary
    "rb", "br",
    # Write binary
    "wb", "bw",
    # Append binary
    "ab", "ba",
    # Exclusive creation binary
    "xb", "bx",
    # Read and write binary
    "rb+", "r+b", "+rb", "br+", "b+r", "+br",
    # Write and read binary
    "wb+", "w+b", "+wb", "bw+", "b+w", "+bw",
    # Append and read binary
    "ab+", "a+b", "+ab", "ba+", "b+a", "+ba",
    # Exclusive creation and read binary
    "xb+", "x+b", "+xb", "bx+", "b+x", "+bx",
    # Universal newline support in binary mode
    "rbU", "rUb", "Urb", "brU", "bUr", "Ubr",
]

type Filename = str | pathlib.Path
type IO = typing.IO[str] | typing.IO[bytes]


class FileOpenKwargs(typing.TypedDict):
    r"""Keyword arguments for opening a file."""

    buffering: int | None
    encoding: str | None
    errors: str | None
    newline: str | None
    closefd: bool | None
    opener: typing.Callable[[str, int], int] | None
