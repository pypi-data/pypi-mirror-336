from typing import Any, Dict, Optional

from overrides import overrides
from sentineltoolbox import eopf_interface

from eopf import EOContainer, EOLogging, EOProduct
from eopf.common.file_utils import AnyPath
from eopf.store.mapping_manager import EOPFAbstractMappingManager
from eopf.store.safe import EOSafeInit


class SentinelToolBoxSafeInit(EOSafeInit):
    """
    Bind the sentinel toolbox converter to the SafeStore

    .. code-block:: JSON

            "init_function": {
                   "module" : "eopf.store.sentineltoolbox_bindings",
                   "class" : "SentinelToolBoxSafeInit"
            },

    """

    def init_container(
        self,
        url: AnyPath,
        name: str,
        attrs: Dict[str, Any],
        product_type: str,
        processing_version: str,
        mapping: Optional[dict[str, Any]],
        mapping_manager: EOPFAbstractMappingManager,
        **eop_kwargs: Any,
    ) -> EOContainer:
        raise NotImplementedError("Container mode not implement in this init class")

    @overrides
    def init_product(
        self,
        url: AnyPath,
        name: str,
        attrs: Dict[str, Any],
        product_type: str,
        processing_version: str,
        mapping: Optional[dict[str, Any]],
        mapping_manager: EOPFAbstractMappingManager,
        **eop_kwargs: Any,
    ) -> EOProduct:
        logger = EOLogging().get_logger("eopf.store.sentineltoolbox")
        logger.info(f"Using sentineltoolbox to load {url.__repr__()} : {type(url)}")

        # TODO : remove the .path once sentineltoolbox stops using original_url
        dtree = eopf_interface.convert_safe_to_datatree(url.path, product_type=product_type, attrs=attrs, name=name)

        return EOProduct.from_datatree(dtree)
