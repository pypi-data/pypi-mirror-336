"""
monarchtominttoreport
"""

from . import convert
from convert import convert_csv as convert_csv
from convert import write_mint_csv as write_mint_csv

__version__ = "0.2a4"
__all__ = ["convert", "convert_csv", "write_mint_csv"]

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("monarchtominttoreport")
except PackageNotFoundError:
    # package is not installed
    pass