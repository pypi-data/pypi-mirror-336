"""Earth Observation Platform Core Python Modules"""

from .common import OpeningMode
from .config import EOConfiguration
from .logging import EOLogging
from .product.eo_container import EOContainer
from .product.eo_group import EOGroup
from .product.eo_product import EOProduct
from .product.eo_variable import EOVariable
from .store.cog import EOCogStore
from .store.convert import convert
from .store.netcdf import EONetCDFStore
from .store.safe import EOSafeStore
from .store.zarr import EOZarrStore

# More features to be imported and listed here
__all__ = [
    "EOProduct",
    "EOVariable",
    "EOGroup",
    "EOContainer",
    "EOSafeStore",
    "EOZarrStore",
    "EONetCDFStore",
    "EOCogStore",
    "convert",
    "EOConfiguration",
    "EOLogging",
    "OpeningMode",
]
__version__ = "2.5.6"
