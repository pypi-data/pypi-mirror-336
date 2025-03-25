import re

import fsspec


def fs_match_path(pattern: str, filesystem: fsspec.FSMap) -> str:
    """Find and return the first occurrence of a path matching
    a given pattern.

    If there is no match, pattern is return as it is.

    Parameters
    ----------
    pattern: str
        regex pattern to match
    filesystem    filesystem representation

    Returns
    -------
    str
        matching path if find, else `pattern`
    """
    filepath_regex = re.compile(pattern)
    for file_path in filesystem:
        if filepath_regex.fullmatch(file_path):
            return file_path
    return pattern
