from typing import Any

from .abstract import EOAbstractFormatter


class ToImageSize(EOAbstractFormatter):
    """Silent Formatter used to read metadata files"""

    # docstr-coverage: inherited
    name = "to_imageSize"

    def _format(self, input: Any) -> Any:
        """Silent formatter, used only for parsing the path
        logic is present in stac_mapper method of XMLManifestAccessor

        Parameters
        ----------
        input: Any
            input

        Returns
        ----------
        Any:
            Returns the input
        """
        return input


class Text(EOAbstractFormatter):
    """Silent Formatter used to read metadata files"""

    # docstr-coverage: inherited
    name = "Text"

    def _format(self, input: Any) -> Any:
        """Silent formatter, used only for parsing the path
        logic is present in stac_mapper method of XMLManifestAccessor

        Parameters
        ----------
        input: Any
            input

        Returns
        ----------
        Any:
            Returns the input
        """
        return input
