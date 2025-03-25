import contextlib
import os
from typing import Any, ContextManager, Iterator


@contextlib.contextmanager
def env_context(environ: dict[str, str]) -> Iterator[None]:
    """Context that temporarily register the process environment variables."""
    old_environement = os.environ.copy()
    os.environ.update(environ)
    try:
        yield os.environ
    finally:
        os.environ.clear()
        os.environ.update(old_environement)


def env_context_eopf() -> ContextManager[None]:
    import eopf

    eopf_path = os.path.dirname(eopf.__file__)
    return env_context({"EOPF_ROOT": eopf_path})


def resolve_env_vars(data: Any) -> Any:
    """
    Recursively resolve env var in dict/str etc
    """
    if isinstance(data, dict):
        resolved_data = {}
        for key, value in data.items():
            resolved_key = resolve_env_vars(key)
            resolved_value = resolve_env_vars(value)
            resolved_data[resolved_key] = resolved_value
        return resolved_data
    elif isinstance(data, list):
        return [resolve_env_vars(it) for it in data]
    elif isinstance(data, str):
        return os.path.expandvars(data)
    else:
        return data
