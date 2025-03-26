"""Theia dumper package."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("theia_dumper")
except PackageNotFoundError:
    pass
