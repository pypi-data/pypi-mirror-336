from re import search
from typing import Any, List

import lxml.etree
import numpy

from eopf.exceptions import FormattingError
from eopf.logging import EOLogging

from .abstract import EOAbstractXMLFormatter


class ToBands(EOAbstractXMLFormatter):
    name = "to_bands"

    def _format(self, xpath_input: List[lxml.etree._Element]) -> List[int]:
        bands_set = set()
        for element in xpath_input:
            band_id = int(element.attrib["bandId"])
            bands_set.add(band_id)
        return sorted(bands_set)


class ToDetectors(EOAbstractXMLFormatter):
    name = "to_detectors"

    def _format(self, xpath_input: List[lxml.etree._Element]) -> List[int]:
        detectors_set = set()
        for element in xpath_input:
            detector_id = int(element.attrib["detectorId"])
            detectors_set.add(detector_id)

        return sorted(detectors_set)


class ToMean(EOAbstractXMLFormatter):
    name = "to_mean"

    def _format(self, xpath_input: List[lxml.etree._Element]) -> Any:
        return numpy.mean([float(element.text) for element in xpath_input])


class ToList(EOAbstractXMLFormatter):
    name = "to_list"

    def _format(self, xpath_input: List[lxml.etree._Element]) -> Any:
        return [float(element.text) for element in xpath_input]


class ToListStr(EOAbstractXMLFormatter):
    name = "to_list_str"

    def _format(self, xpath_input: List[lxml.etree._Element]) -> Any:
        return [element for element in xpath_input]


class ToListFloat(EOAbstractXMLFormatter):
    name = "to_list_float"

    def _format(self, xpath_input: List[lxml.etree._Element]) -> Any:
        return [float(element) for element in xpath_input]


class ToListInt(EOAbstractXMLFormatter):
    name = "to_list_int"

    def _format(self, xpath_input: List[lxml.etree._Element]) -> Any:
        return [int(element) for element in xpath_input]


class ToProcessingHistory(EOAbstractXMLFormatter):
    # docstr-coverage: inherited
    name = "to_processing_history"
    _logger = EOLogging().get_logger("eopf.store.formatters.xml_formatters")

    def get_attr(self, node: Any, path: str) -> Any:
        try:
            childs = node.xpath(path, namespaces=self.namespaces)
        except lxml.etree.XPathEvalError:
            childs = []
            self._logger.warning("The product history is probaly missing namespaces.")
        if len(childs) > 0:
            return str(childs[0])
        else:
            return None

    def transform(self, output: Any, output_role: Any, node: Any, accu: Any) -> str:
        if node is not None:
            processor = self.get_attr(node, f"{self.safe_namespace}:facility/{self.safe_namespace}:software/@name")
            version = self.get_attr(node, f"{self.safe_namespace}:facility/{self.safe_namespace}:software/@version")
            facility_name = self.get_attr(node, f"{self.safe_namespace}:facility/@name")
            facility_organisation = self.get_attr(node, f"{self.safe_namespace}:facility/@organisation")
            processing_time = self.get_attr(node, "@stop")
            inputs: Any = dict()
            try:
                childs = node.xpath(f"{self.safe_namespace}:resource", namespaces=self.namespaces)
            except lxml.etree.XPathEvalError:
                childs = []
                self._logger.warning("The product history is probaly missing namespaces.")
            for child in childs:
                role = self.get_attr(child, "@role")
                input = self.transform(
                    self.get_attr(child, "@name"),
                    self.get_attr(child, "@role"),
                    (
                        child.xpath(f"{self.safe_namespace}:processing", namespaces=self.namespaces)[0]
                        if len(child.xpath(f"{self.safe_namespace}:processing", namespaces=self.namespaces)) > 0
                        else None
                    ),
                    accu,
                )
                if input == "":
                    continue
                if role in inputs:
                    inputs[role + "1"] = inputs.pop(role)
                    inputs[role + "2"] = input
                elif role + "1" in inputs:
                    for i in range(3, 999):
                        if not role + str(i) in inputs:
                            inputs[role + str(i)] = input
                            break
                        if i > 997:
                            raise FormattingError("too many inputs with identical role " + role + " for " + output)
                else:
                    inputs[role] = input
            record = dict()
            record["type"] = output_role
            record["processor"] = processor
            if version:
                record["version"] = version
            if facility_name and facility_organisation:
                record["processingCentre"] = facility_name + ", " + facility_organisation
            if processing_time:
                record["processingTime"] = processing_time
            if len(inputs) > 0:
                record["inputs"] = inputs
            record["output"] = output
            accu.append(record)
        else:
            pass
        return output

    def _format(self, packed_data) -> Any:  # type: ignore
        """

        Parameters
        ----------
        input: Any
            input

        Returns
        ----------
        Any:
            Returns the input
        """
        xml_node, self.namespaces, product_name, url = packed_data

        # S1 namespaces differs from S2 and S4
        s1_rex = r"S1[ABCD]_.{2}_.{4}_(\d).{3}_.*"
        if search(s1_rex, url):
            self.safe_namespace = "safe"
        else:
            self.safe_namespace = "sentinel-safe"

        accu: List[Any] = list()

        # determine the product level based on the url of the product
        level = ""
        if url is not None:
            # Sentinels 1, 2, 3 regexes to retrieve the level
            sentinels_rex = [
                r"S1[ABCD]_.{2}_.{4}_(\d).{3}_.*",
                r"S2[ABCD]_MSI(\w{3})_.*",
                r"S3[ABCD]_\w{2}_(.)_.*",
            ]
            i = 0
            while level == "" and i < len(sentinels_rex):
                match = search(sentinels_rex[i], url)
                if match and match[1]:
                    if match[1][0] != "L":
                        level = "L" + match[1]
                    else:
                        level = match[1]
                else:
                    # in case of no match proceed to the following regex
                    i += 1

        self.transform(
            product_name,
            level,
            xml_node,
            accu,
        )
        return accu


class ToBoolInt(EOAbstractXMLFormatter):
    """Formatter for converting a string to an integer representation of bool"""

    # docstr-coverage: inherited
    name = "to_bool_int"

    def _format(self, xpath_input: Any) -> int:
        low_input = xpath_input[0].lower()
        if low_input in ["true"]:
            return 1
        else:
            return 0


class ToProcessingSoftware(EOAbstractXMLFormatter):
    """Formatter for extracting processing software from xml"""

    # docstr-coverage: inherited
    name = "to_processing_software"
    _logger = EOLogging().get_logger("eopf.store.formatters.xml_formatters")

    def _format(self, xpath_input: Any) -> dict[str, str]:
        # retrieve the name and version of the xml node xpath_input

        try:
            data = xpath_input.attrib
        except Exception as e:
            self._logger.warning(f"Can not retrieve processing:software : {e}")
            data = {"name": "", "version": ""}

        return data


class ToSciDOI(EOAbstractXMLFormatter):
    """Formatter for extracting product doi from xml"""

    # docstr-coverage: inherited
    name = "to_sci_doi"
    _logger = EOLogging().get_logger("eopf.store.formatters.xml_formatters")

    def _format(self, xpath_input: Any) -> str:
        # retrieve the right part of the DOI url
        try:
            if xpath_input and len(xpath_input) == 0:
                data = xpath_input.replace("https://doi.org/", "")
            elif xpath_input and len(xpath_input) == 1:
                data = xpath_input[0].replace("https://doi.org/", "")
        except Exception as e:
            self._logger.warning(f"Can not retrieve sci:doi : {e}")
            data = ""
        return data


class ToProductTimeliness(EOAbstractXMLFormatter):
    """Formatter for getting the timeliness for specific timeliness"""

    # docstr-coverage: inherited
    name = "to_product_timeliness"
    _logger = EOLogging().get_logger("eopf.store.formatters.xml_formatters")

    def _format(self, xpath_input: Any) -> str:

        # read https://github.com/stac-extensions/product/blob/main/README.md
        # to be modified based on what is present in xml_accessors.py workaround of this accessor: TODO
        timeliness_category = xpath_input
        to_timeliness_map = {
            "NR": "PT3H",
            "NRT": "PT3H",
            "NRT-3h": "PT3H",
            "ST": "PT36H",
            "24H": "PT24H",
            "STC": "PT36H",
            "Fast-24h": "PT24H",
            "AL": "Null",
            "NT": "P1M",
            "NTC": "P1M",
        }
        return to_timeliness_map[timeliness_category]


class ToSatOrbitState(EOAbstractXMLFormatter):
    """Formatter for getting the correct orbit state"""

    # docstr-coverage: inherited
    name = "to_sat_orbit_state"
    _logger = EOLogging().get_logger("eopf.store.formatters.xml_formatters")

    def _format(self, xpath_input: Any) -> str:
        """There are cases when that xml data is with uppercase or
        it has several xml data attributes about ascending, descending, etc"""

        data = xpath_input

        # the data might come in uppercase | has usage for S1 products
        if data and len(data) == 1:
            return data[0].lower()
        return "No data about orbit state"


class ToProviders(EOAbstractXMLFormatter):
    """Formatter for respecting providers stac standard"""

    # docstr-coverage: inherited
    name = "to_providers"
    _logger = EOLogging().get_logger("eopf.store.formatters.xml_formatters")

    def _format(self, xpath_input: Any) -> str:
        """The name and organization have to be mentioned as attributes even though there is no info"""
        return xpath_input if xpath_input else "No data about provider"


class ToPlatform(EOAbstractXMLFormatter):
    """Formatter for the platform attribute compliant with the stac standard"""

    # docstr-coverage: inherited
    name = "to_platform"

    def _format(self, xpath_input: List[str]) -> Any:
        """The platform's name retrived from the resulted list from XML search"""
        if isinstance(xpath_input, list) and xpath_input:
            return xpath_input[0].lower()
        elif isinstance(xpath_input, str) and xpath_input:
            return xpath_input.lower()
        else:
            raise FormattingError("No data about stac_discovery/properties/platform")


class ToSarPolarizations(EOAbstractXMLFormatter):
    """Formatter for sar:polarizations attribute"""

    # docstr-coverage: inherited
    name = "to_sar_polarizations"

    def _format(self, xpath_input: list[str]) -> Any:
        """The input parameter from this function should be a list with all polarizations"""
        if isinstance(xpath_input, list):
            return xpath_input
        else:
            raise FormattingError("The xml path for sar:polarizations is wrong or it doesn't exist!")
