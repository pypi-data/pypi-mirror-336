from typing import List, Optional


def join_path(*subpath: str, sep: str = "/") -> str:
    """Join elements from specific separator

    Parameters
    ----------
    *subpath: str
    sep: str, optional
        separator

    Returns
    -------
    str
    """
    return sep.join(subpath)


def regex_path_append(path1: Optional[str], path2: Optional[str]) -> Optional[str]:
    """Append two (valid) regex path.
    Can use os/eo path append as regex path syntax is different.
    """
    if path1 is not None:
        path1 = path1.removesuffix("/")
    if path2 is None:
        return path1
    path2 = path2.removeprefix("/")
    if path1 is None:
        return path2
    return f"{path1}/{path2}"


def remove_specific_extensions(path: str, exts: List[str]) -> str:
    for suffix in exts:
        path = path.removesuffix(suffix)
    return path


def add_extension(path: str, extension: str) -> str:
    return path + extension
