"""The store package provides stores that allow reading and writing the EOProducts.

All stores are based on the main abstract EOProductStore class.
"""

from eopf.store.abstract import EOProductStore, EOReadOnlyStore, StorageStatus

__all__ = [
    "EOProductStore",
    "StorageStatus",
    "EOReadOnlyStore",
]
