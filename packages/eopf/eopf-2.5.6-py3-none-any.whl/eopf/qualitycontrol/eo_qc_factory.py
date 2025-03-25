from typing import Any, Callable, Type

import dacite
import numpy as np
from dacite import Config, MissingValueError

from eopf.exceptions.errors import EOQCError
from eopf.qualitycontrol.eo_qc import EOQC


class EOQCFactory:
    qc_dict: dict[str, Type[EOQC]] = dict()

    def __new__(cls, *args: Any, **kwargs: Any) -> None:
        raise TypeError("EOStoreFactory can not be instantiated : static class !!")

    @classmethod
    def register_eoqc(cls, name: str) -> Callable[[Type[EOQC]], Type[EOQC]]:
        """
        Register an EOQC in the factory
        Parameters
        ----------
        name

        Returns
        -------

        """

        def inner_register(wrapped: Type[EOQC]) -> Type[EOQC]:
            cls.qc_dict[name] = wrapped
            return wrapped

        return inner_register

    @classmethod
    def get_eoqc_type(cls, eoqc_name: str) -> Type[EOQC]:
        """
        Get the EOQC for this name

        Parameters
        ----------
        eoqc_name

        Returns
        -------

        """
        if eoqc_name in cls.qc_dict:
            return cls.qc_dict[eoqc_name]
        raise KeyError(f"No registered eoqc with name : {eoqc_name}")

    @classmethod
    def get_eoqc_instance(cls, eoqc_name: str, data: dict[str, Any]) -> EOQC:
        """
        Get the EOQC for this name

        Parameters
        ----------
        data
        eoqc_name

        Returns
        -------

        """
        eoqc_type = EOQCFactory.get_eoqc_type(eoqc_name)
        try:
            eoqc = dacite.from_dict(eoqc_type, data, config=Config(type_hooks={np.float64: lambda x: np.float64(x)}))
        except MissingValueError as e:
            raise EOQCError(f"Missing element in configuration to instance {eoqc_type} : {e}") from e
        return eoqc

    @classmethod
    def get_eoqc_available(cls) -> dict[str, Type[EOQC]]:
        out_dict = {}
        for name, val in cls.qc_dict.items():
            out_dict[f"{name}"] = val
        return out_dict

    @classmethod
    def check_eoqc_available(cls, name: str) -> bool:
        return name in cls.qc_dict
