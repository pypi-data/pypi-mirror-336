from typing import Any, Optional

from eopf import EOContainer, EOProduct
from eopf.common.file_utils import AnyPath
from eopf.store.mapping_manager import EOPFAbstractMappingManager
from eopf.store.safe import EOSafeFinalize  # import first


class DefaultFinalizeClass(EOSafeFinalize):

    def finalize_product(
        self,
        eop: EOProduct,
        url: AnyPath,
        mapping: Optional[dict[str, Any]],
        mapping_manager: EOPFAbstractMappingManager,
        **eop_kwargs: Any,
    ) -> None:
        pass

    def finalize_container(
        self,
        container: EOContainer,
        url: AnyPath,
        mapping: Optional[dict[str, Any]],
        mapping_manager: EOPFAbstractMappingManager,
        **eop_kwargs: Any,
    ) -> None:

        # duplicate and merge attributes into subproducts
        for _, product in container.items():
            product_attrs = {
                "other_metadata": container.attrs["other_metadata"] | product.attrs.get("other_metadata", {}),
                "stac_discovery": container.attrs["stac_discovery"] | product.attrs.get("stac_discovery", {}),
            }
            product.attrs = product_attrs
