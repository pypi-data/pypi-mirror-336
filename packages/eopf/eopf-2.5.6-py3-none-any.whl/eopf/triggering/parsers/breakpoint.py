from typing import Any

from eopf.triggering.parsers.general import EOTriggeringKeyParser, parse_store_params


class EOBreakPointParser(EOTriggeringKeyParser):
    """breakpoints section Parser"""

    KEY = "breakpoints"
    MANDATORY_KEYS = ("ids",)
    OPTIONAL_KEYS = ("folder", "all", "store_params")
    OPTIONAL = True
    DEFAULT: dict[str, Any] = {}

    def _parse(self, data_to_parse: Any, **kwargs: Any) -> tuple[Any, list[str]]:
        errors = self.check_mandatory(data_to_parse) + self.check_unknown(data_to_parse)
        if errors:
            return None, errors
        ids = data_to_parse.get("ids")
        if not isinstance(ids, list):
            return {}, [f"breakpoints misconfigured, ids should be a list, but is {type(ids)}"]

        return {
            "ids": ids,
            "all": data_to_parse.get("all", False),
            "folder": data_to_parse.get("folder", None),
            "store_params": parse_store_params(data_to_parse.get("store_params", {}))["storage_options"],
        }, errors

    def parse(self, data_to_parse: Any, **kwargs: Any) -> Any:
        result = super().parse(data_to_parse, **kwargs)
        if isinstance(result, list) and len(result) > 0:
            return result[0]
        return result
