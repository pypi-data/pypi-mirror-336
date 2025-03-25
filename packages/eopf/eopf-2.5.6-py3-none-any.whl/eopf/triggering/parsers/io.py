import enum
from abc import ABC
from typing import Any, Optional, Type

from eopf import OpeningMode
from eopf.common.file_utils import AnyPath
from eopf.exceptions import TriggeringConfigurationError
from eopf.store.abstract import EOProductStore
from eopf.store.store_factory import EOStoreFactory
from eopf.triggering.parsers.general import EOTriggeringKeyParser, parse_store_params


class PathType(enum.Enum):
    Filename = "filename"
    Folder = "folder"
    Regex = "regex"


class ProductStoreParser(EOTriggeringKeyParser, ABC):
    @staticmethod
    def get_store_driver_cls(
        path: Optional[str] = None,
        store_type: Optional[str] = None,
        **kwargs: Any,
    ) -> Type[EOProductStore]:
        """Instantiate an EOProductStore from the given inputs

        Parameters
        ----------
        path: str
            path to the corresponding product
        store_type: str
            key for the EOStoreFactory to retrieve the correct type of store

        Returns
        -------
        Type[EOProductStore]

        See Also
        --------
        eopf.product.store.EOProductStore
        eopf.product.store.store_factory.EOStoreFactory
        """
        if store_type is not None:
            return EOStoreFactory.get_product_store_by_format(store_type)
        if path is not None:
            fspath: AnyPath = AnyPath.cast(path, kwargs=kwargs)
            return EOStoreFactory.get_product_store_by_file(fspath)
        raise TriggeringConfigurationError("Either path or store_type requested")


class EOOutputProductStoreParser(ProductStoreParser):
    """I/O output section Parser"""

    KEY = "output_products"
    MANDATORY_KEYS = ("id", "path", "store_type")
    OPTIONAL_KEYS = ("store_params", "type", "opening_mode", "apply_eoqc")

    def _parse(self, data_to_parse: Any, **kwargs: Any) -> tuple[Any, list[str]]:
        errors = self.check_mandatory(data_to_parse) + self.check_unknown(data_to_parse)
        store_type = data_to_parse.get("store_type")
        if errors:
            return None, errors
        # Check if the store is valid
        if store_type and not EOStoreFactory.check_product_store_available(store_type):
            errors.append(
                f"{store_type=} not recognized, should be one of "
                f"{tuple(EOStoreFactory.get_product_stores_available().keys())}.",
            )
            return None, errors
        # Check the opening mode, Open is not valid
        opening_mode = OpeningMode[data_to_parse.get("opening_mode", "CREATE")]
        if opening_mode not in (
            OpeningMode.CREATE,
            OpeningMode.CREATE_OVERWRITE,
            OpeningMode.CREATE_NO_OVERWRITE,
            OpeningMode.UPDATE,
        ):
            errors.append(
                f"{opening_mode} not allowed, should be one of "
                f"{(OpeningMode.CREATE, OpeningMode.CREATE_OVERWRITE, OpeningMode.UPDATE)}.",
            )
            return None, errors
        store_params = parse_store_params(data_to_parse.get("store_params", {}))
        data_parsed = {
            "id": data_to_parse.get("id"),
            "store_class": self.get_store_driver_cls(**data_to_parse),
            "path": AnyPath.cast(data_to_parse.get("path"), **store_params["storage_options"]),
            "type": PathType(data_to_parse.get("type", "filename")),
            "opening_mode": OpeningMode[data_to_parse.get("opening_mode", "CREATE")],
            "store_type": data_to_parse.get("store_type"),
            "store_params": store_params,
            "apply_eoqc": bool(data_to_parse.get("apply_eoqc", False)),
        }
        return data_parsed, errors


class EOInputProductParser(ProductStoreParser):
    """I/O inputs_products section Parser"""

    KEY = "input_products"
    MANDATORY_KEYS = ("id", "path", "store_type")
    OPTIONAL_KEYS = (
        "store_params",
        "type",
    )

    def _parse(self, data_to_parse: Any, **kwargs: Any) -> tuple[Any, list[str]]:
        errors = self.check_mandatory(data_to_parse) + self.check_unknown(data_to_parse)
        store_type = data_to_parse.get("store_type")

        if store_type and not EOStoreFactory.check_product_store_available(store_type):
            errors.append(
                f"{store_type=} not recognized, should be one of "
                f"{tuple(EOStoreFactory.get_product_stores_available().keys())}.",
            )
        if errors:
            return None, errors

        store_params = parse_store_params(data_to_parse.get("store_params", {}))
        data_parsed = {
            "id": data_to_parse.get("id"),
            "store_class": self.get_store_driver_cls(**data_to_parse),
            "path": AnyPath.cast(data_to_parse.get("path"), **store_params["storage_options"]),
            "type": PathType(data_to_parse.get("type", "filename")),
            "store_type": data_to_parse.get("store_type"),
            "store_params": store_params,
        }
        return data_parsed, errors


class EOADFStoreParser(EOTriggeringKeyParser):
    KEY = "adfs"
    OPTIONAL = True
    MANDATORY_KEYS = ("id", "path")
    OPTIONAL_KEYS = ("store_params",)
    DEFAULT: list[dict[str, Any]] = []

    def _parse(self, data_to_parse: Any, **kwargs: Any) -> tuple[Any, list[str]]:
        errors = self.check_mandatory(data_to_parse) + self.check_unknown(data_to_parse)

        if errors:
            return None, errors
        store_params = parse_store_params(data_to_parse.get("store_params", {}))
        data_parsed = {
            "id": data_to_parse.get("id"),
            "path": AnyPath.cast(data_to_parse.get("path"), **store_params["storage_options"]),
            "store_params": store_params,
        }
        return data_parsed, errors


class EOIOParser(EOTriggeringKeyParser):
    """I/O section Parser"""

    KEY = "I/O"
    MANDATORY_KEYS = ("input_products", "output_products")
    OPTIONAL_KEYS = ("adfs",)

    def _parse(self, data_to_parse: Any, **kwargs: Any) -> Any:
        errors = self.check_mandatory(data_to_parse) + self.check_unknown(data_to_parse)
        if errors:
            return None, errors

        loaded_io_config: dict[str, Any] = {
            "output_products": EOOutputProductStoreParser().parse(data_to_parse),
            "input_products": EOInputProductParser().parse(data_to_parse),
            "adfs": EOADFStoreParser().parse(data_to_parse),
        }
        return loaded_io_config, errors

    def parse(self, data_to_parse: Any, **kwargs: Any) -> Any:
        return super().parse(data_to_parse, **kwargs)[0]
