import os.path
from typing import Any

from eopf.triggering.parsers.general import EOTriggeringKeyParser


class EOLoggingConfParser(EOTriggeringKeyParser):
    KEY: str = "logging"
    OPTIONAL: bool = True
    DEFAULT: list[str] = []
    LOAD_JSON: bool = False

    def _parse(self, data_to_parse: Any, **kwargs: Any) -> tuple[Any, list[str]]:
        if data_to_parse is None:
            return self.DEFAULT, []
        if not isinstance(data_to_parse, str):
            return self.DEFAULT, [f"logging misconfigured, should be a str, but is {type(data_to_parse)}"]
        return os.path.expandvars(data_to_parse), []

    def parse(self, data_to_parse: Any, **kwargs: Any) -> dict[str, Any]:
        data = super().parse(data_to_parse, **kwargs)
        return data
