from typing import Any

from eopf.triggering.parsers.general import EOTriggeringKeyParser


class EOGeneralConfigurationParser(EOTriggeringKeyParser):
    KEY: str = "general_configuration"
    OPTIONAL: bool = True
    DEFAULT: dict[str, Any] = {}
    LOAD_JSON: bool = False

    def _parse(self, data_to_parse: Any, **kwargs: Any) -> tuple[Any, list[str]]:
        if data_to_parse is None:
            return self.DEFAULT, []
        if not isinstance(data_to_parse, dict):
            return self.DEFAULT, [f"config misconfigured, should be a dict, but is {type(data_to_parse)}"]
        return data_to_parse, []

    def parse(self, data_to_parse: Any, **kwargs: Any) -> dict[str, Any]:
        data = super().parse(data_to_parse, **kwargs)
        return data
