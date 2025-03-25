from typing import Any

from eopf.triggering.parsers.general import EOTriggeringKeyParser


class EOExternalModuleImportParser(EOTriggeringKeyParser):
    KEY: str = "external_modules"
    OPTIONAL: bool = True
    MANDATORY_KEYS = ("name",)
    OPTIONAL_KEYS = ("alias", "nested")
    DEFAULT: list[str] = []
    LOAD_JSON: bool = False

    def _parse(self, data_to_parse: Any, **kwargs: Any) -> tuple[Any, list[str]]:
        errors = self.check_mandatory(data_to_parse) + self.check_unknown(data_to_parse)
        if errors:
            return None, errors

        data_parsed = {
            "name": data_to_parse.get("name"),
            "alias": data_to_parse.get("alias", None),
            "nested": data_to_parse.get("nested", None),
        }
        return data_parsed, errors
