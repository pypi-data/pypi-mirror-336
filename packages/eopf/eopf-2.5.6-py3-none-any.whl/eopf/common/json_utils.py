from numbers import Number
from typing import Any, Mapping

import xarray

from eopf.common.type_utils import convert_to_native_python_type

RESTRICTED_ATTRS = ["_ARRAY_DIMENSIONS"]


def decode_all_attrs(attrs_map: Mapping[str, Any]) -> dict[str, Any]:
    """For each attribute try to decode it if it is a json,
    otherwise return the attr as it is

    Parameters
    ----------
    attrs: Mapping[str, Any]
        mapping of attributes or a json dumps of an attribute

    Returns
    ----------
    dict[str, Any]
        the attributes
    """
    return {key: decode_attr(value) for key, value in attrs_map.items()}


def decode_attr(attr: Any) -> Any:
    """Try to decode an attribute as json if possible,
    otherwise return the attr as it is

    Parameters
    ----------
    attrs: Any
        an attribute or a json dump of an attribute

    Returns
    ----------
    Any
        the attribute
    """
    from json import JSONDecodeError, loads

    try:
        new_attrs = loads(attr)
    except (JSONDecodeError, TypeError):
        return attr
    return new_attrs


def encode_all_attrs(attrs_map: Mapping[str, Any]) -> dict[str, Any]:
    """Encode all attribute in json as needed,
    otherwise return the attr as it is

    Parameters
    ----------
    attrs: Any
        an attribute

    Returns
    ----------
    Any
        either the attributes as json or the attributes as received
    """
    conv_attr = dict()
    for attr, attr_value in attrs_map.items():
        attr_value = encode_attr(attr_value)
        if attr not in RESTRICTED_ATTRS:
            conv_attr[attr] = attr_value
    return conv_attr


def encode_attr(attr: Any) -> Any:
    """Encode an attribute as json if needed,
    otherwise return the attr as it is

    Parameters
    ----------
    attrs: Any
        an attribute

    Returns
    ----------
    Any
        either the attributes as json or the attributes as received
    """
    from json import dumps

    attr = convert_to_native_python_type(attr)
    if isinstance(attr, str) or isinstance(attr, Number):
        return attr
    if isinstance(attr, xarray.DataArray):
        return attr.to_numpy()
    return dumps(attr)
