import contextlib
from typing import Any, Iterator

from eopf.accessor import EOAccessor
from eopf.common.constants import OpeningMode
from eopf.logging import EOLogging


@contextlib.contextmanager
def open_accessor(accessor: EOAccessor, mode: OpeningMode = OpeningMode.OPEN, **kwargs: Any) -> Iterator[EOAccessor]:
    """Open an EOAccessor in the given mode.

    help you to open EOAccessor
    it as a standard python open function.

    Parameters
    ----------
    accessor: EOAccessor
        accessor to open
    mode: str, optional
        mode to open the store (default = 'r')
    kwargs: any
        store specific kwargs

    Returns
    -------
    store
        store opened with given arguments

    See Also
    --------
    EOProductStore.open
    """
    logger = EOLogging().get_logger("eopf.accessor.conveniences")
    try:
        logger.debug(f"Opening : {accessor}")
        accessor.open(mode=mode, **kwargs)
        yield accessor
    finally:
        accessor.close()
