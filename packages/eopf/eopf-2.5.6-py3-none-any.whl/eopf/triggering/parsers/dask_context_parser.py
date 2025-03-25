from contextlib import nullcontext
from typing import Any

from eopf.daskconfig import DaskContext
from eopf.daskconfig.dask_context_manager import get_enum_from_value
from eopf.triggering.parsers.general import EOTriggeringKeyParser


class EODaskContextParser(EOTriggeringKeyParser):
    """Dask context Parser"""

    KEY = "dask_context"
    OPTIONAL = True
    OPTIONAL_KEYS = ("cluster_type", "address", "cluster_config", "client_config", "performance_report_file")
    MANDATORY_KEYS = ()
    DEFAULT = nullcontext()

    def _parse(self, data_to_parse: Any, **kwargs: Any) -> tuple[Any, list[str]]:
        if data_to_parse is None:
            return {}, []
        if not isinstance(data_to_parse, dict):
            return None, [f"dask context misconfigured, should be dict, but is {type(data_to_parse)}"]
        errors = self.check_mandatory(data_to_parse) + self.check_unknown(data_to_parse)
        if errors:
            return None, errors
        if "cluster_type" not in data_to_parse and "address" not in data_to_parse:
            return None, ["address dask context parameter should be provided when no cluster type given"]

        data_parsed = {
            "cluster_type": get_enum_from_value(str(data_to_parse.get("cluster_type", "address"))),
            "address": data_to_parse.get("address", None),
            "cluster_config": data_to_parse.get("cluster_config", None),
            "client_config": data_to_parse.get("client_config", None),
            "performance_report_file": data_to_parse.get("performance_report_file", None),
        }
        return DaskContext(**data_parsed), errors

    def parse(self, data_to_parse: Any, **kwargs: Any) -> Any:
        result = super().parse(data_to_parse, **kwargs)
        if isinstance(result, list) and len(result) > 0:
            return result[0]
        return result
