"""
monarchtominttoreport
"""
#from monarchtominttoreport.convert import convert_csv as convert_csv
#from monarchtominttoreport.convert import write_mint_csv as write_mint_csv

__version__ = "0.2a3"
__all__ = ["convert"]

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("monarchtominttoreport")
except PackageNotFoundError:
    # package is not installed
    pass