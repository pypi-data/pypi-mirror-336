from dataclasses import dataclass, field
from typing import Any

from eopf import EOProduct
from eopf.common.functions_utils import resolve_path_in_dict, safe_eval


@dataclass
class EOQCFormulaEvaluator:
    """Formula evaluator.

    Parameters
    ----------
    formula: str
        Formula to execute.
    parameters: dict[str, Any]
        The different parameters use in the formula.
    variables: dict[str, Any]
        The different variables use in the formula.
    attributes: dict[str, Any]
       The different attributes use in the formula.

    Attributes
    ----------
    formula: str
        Formula to execute.
    parameters: dict[str, Any]
        The different thresholds use in the formula.
    variables: dict[str, Any]
        The different variables use in the formula.
    attributes: dict[str, Any]
       The different attributes use in the formula.
    """

    SECURITY_TOKEN = ["rm"]

    formula: str = "True"
    parameters: list[dict[str, Any]] = field(default_factory=list)
    variables: list[dict[str, Any]] = field(default_factory=list)
    attributes: list[dict[str, Any]] = field(default_factory=list)

    # docstr-coverage: inherited
    def evaluate(self, eoproduct: EOProduct) -> Any:
        # Getting and defining variables/attributes from eoproduct
        local_var = {}
        for variable in self.variables:
            local_var[variable["name"]] = eoproduct[variable["path"]]
        for attribute in self.attributes:
            local_var[attribute["name"]] = resolve_path_in_dict(eoproduct.attrs, attribute["path"])
        # Getting and defining thresholds
        for param in self.parameters:
            local_var[param["name"]] = param["value"]
        # The eoproduct is available under eoproduct
        local_var["eoproduct"] = eoproduct

        # Applying the formula
        return safe_eval(f"{self.formula}", variables=local_var)
