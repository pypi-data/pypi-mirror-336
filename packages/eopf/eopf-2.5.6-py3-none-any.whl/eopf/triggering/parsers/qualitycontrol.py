from typing import Any, Optional

from eopf.triggering.parsers.general import EOTriggeringKeyParser


class EOQualityControlParser(EOTriggeringKeyParser):
    """breakpoints section Parser"""

    KEY = "eoqc"
    OPTIONAL_KEYS = (
        "config_folder",
        "parameters",
        "update_attrs",
        "report_path",
        "config_path",
        "additional_config_folders",
    )
    OPTIONAL = True
    DEFAULT: Optional[dict[str, Any]] = None

    def _parse(self, data_to_parse: Any, **kwargs: Any) -> tuple[Any, list[str]]:
        errors = self.check_mandatory(data_to_parse) + self.check_unknown(data_to_parse)
        if errors:
            return None, errors

        return {
            "config_folder": data_to_parse.get("config_folder", None),
            "parameters": data_to_parse.get("parameters", None),
            "update_attrs": data_to_parse.get("update_attrs", None),
            "report_path": data_to_parse.get("report_path", None),
            "config_path": data_to_parse.get("config_path", None),
        }, errors

    def parse(self, data_to_parse: Any, **kwargs: Any) -> Any:
        result = super().parse(data_to_parse, **kwargs)
        if isinstance(result, list) and len(result) > 0:
            return result[0]
        return result
