import datetime
from typing import Any, Literal, Mapping, Optional, Sequence, Union

import numpy as np

from eopf.common import date_utils


def convert_to_native_python_type(obj: Any) -> Any:
    """Convert an object to native python data types if possible,
    otherwise return the the obj as it is

    Parameters
    ----------
    obj: Any
        an object

    Returns
    ----------
    Any
        either the obj converted to native Python data type,
        or the obj as received
    """
    # check dict
    if isinstance(obj, dict):
        res = {}
        for k, v in obj.items():
            res[k] = convert_to_native_python_type(v)
        return res

    # check if list or tuple or register_requested_parameter
    if isinstance(obj, (list, tuple, set)):
        return type(obj)(map(convert_to_native_python_type, obj))

    # check numpy
    if isinstance(obj, np.ndarray):
        return [convert_to_native_python_type(i) for i in obj.tolist()]

    # check numpy bool_
    if isinstance(obj, np.bool_):
        return bool(obj)

    # check np int
    if isinstance(obj, (*get_managed_numpy_dtype("int"), int)) and not isinstance(obj, bool):
        return int(obj)

    # check np float
    if isinstance(obj, (*get_managed_numpy_dtype("float"), float)):
        return float(obj)

    # check str or datetime-like string
    if isinstance(obj, str):
        return str(obj)

    # check datetime
    if isinstance(obj, datetime.datetime):
        return date_utils.convert_to_unix_time(obj)

    if isinstance(obj, bytes):
        return obj.decode()

    # if no conversion can be done
    return obj


def reverse_conv(data_type: Any, obj: Any) -> Any:
    """Converts the obj to the data_type

    Parameters
    ----------
    data_type: Any
        the data type to be converted to
    obj: Any
        an object

    Returns
    ----------
    Any
    """
    for dtype in get_managed_numpy_dtype():
        if np.dtype(data_type) == np.dtype(dtype):
            return dtype(obj)
    return obj


def get_managed_numpy_dtype(type_: Optional[str] = None) -> tuple[type, ...]:
    """Retrieve OS dependent dtype for numpy"""
    managed_type: dict[str, Sequence[str]] = {"uint": ("uint64", "uint32", "uint16", "uint8")}
    managed_type["int"] = ("int64", "int32", "int16", "int8", *managed_type["uint"])
    managed_type["float"] = ("float64", "float32", "float16")
    if type_:
        types = managed_type.get(type_, tuple())
    else:
        types = [dtype for type_group in managed_type.values() for dtype in type_group]
    return tuple(getattr(np, attr) for attr in types if hasattr(np, attr))


Chunk = Union[
    None,
    int,
    Literal["auto"],
    tuple[int, ...],
    Mapping[Any, int | Literal["auto"] | tuple[int, ...] | None],
]


class Singleton(type):
    _instances: dict[Any, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def clear(cls) -> None:
        cls._instances.pop(cls, None)
