import importlib
import re
from collections import defaultdict
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, List, Optional, Sequence, Union

from eopf.computing import EOProcessingUnit
from eopf.computing.abstract import (
    AuxiliaryDataFile,
    DataType,
    MappingAuxiliary,
    MappingDataType,
)
from eopf.exceptions.errors import TriggerInvalidWorkflow
from eopf.logging import EOLogging
from eopf.triggering.parsers.general import EOTriggeringKeyParser


class Graph:
    """Class to represent a graph of Processing units"""

    def __init__(self, nb_vertices: int) -> None:
        self._graph: defaultdict[Any, Any] = defaultdict(list)  # dictionary containing adjacency List
        self.V = nb_vertices  # Number of vertices

    def add_edge(self, u: Any, v: Any) -> None:
        """Function to add an edge to graph"""

        self._graph[u].append(v)

    def topological_sort_util(self, v: int, visited: List[Any], stack: List[Any]) -> None:
        """A recursive function used by topological sort"""

        # Mark the current node as visited.
        visited[v] = True

        # Recur for all the vertices adjacent to this vertex
        for i in self._graph[v]:
            if visited[i] is False:
                self.topological_sort_util(i, visited, stack)

        # Push current vertex to stack which stores result
        stack.insert(0, v)

    def topological_sort(self) -> List[Any]:
        """The function to do Topological Sort. It uses recursive ``togopologicalSortUtil()``"""

        # Mark all the vertices as not visited
        visited = [False] * self.V
        stack: List[Any] = []

        # Call the recursive helper function to store Topological
        # Sort starting from all vertices one by one
        for i in range(self.V):
            if visited[i] is False:
                self.topological_sort_util(i, visited, stack)

        # reverse the order to get the processing units righ execution order
        stack.reverse()
        return stack

    def has_cyclic_dependency(self) -> bool:
        # Colors to mark the status of each vertex during DFS
        WHITE = 0  # Not visited
        GRAY = 1  # Visited but not finished
        BLACK = 2  # Finished

        def dfs(v: int) -> None:
            nonlocal has_cycle
            visited[v] = GRAY

            for neighbor in self._graph[v]:
                if visited[neighbor] == WHITE:
                    dfs(neighbor)
                elif visited[neighbor] == GRAY:
                    has_cycle = True

            visited[v] = BLACK

        # Initialize visited array
        visited = [WHITE] * self.V
        has_cycle = False

        # Start DFS from each unvisited node
        for node in range(self.V):
            if visited[node] == WHITE:
                dfs(node)

        return has_cycle


@dataclass
class WorkFlowUnitDescription:
    """Dataclass used to wrap EOProcessingUnit for triggering execution"""

    active: bool
    """ Is the unit activated """
    processing_unit: EOProcessingUnit
    """Wrapped EOProcessingUnit"""
    inputs: dict[str, str]
    """ Description of the inputs to use::

        "inputs": {
                    "processing_unit_input_name" : "I/O input id" | "source_processing_unit_name.outputname"
                   }

    """
    adfs: dict[str, str]
    """ Description of the input adfs to use::

        "adfs": {
                    "adf_input_name" : "I/O adf id"
                   }

    """
    outputs: dict[str, str]
    """ Description of the outputs to write::

        "outputs": { "processing_unit_output_name" : {"id" : "I/O id"} }

    """
    parameters: dict[str, Any]
    """all kwargs to use a execution time"""

    step: int
    """ Step integer number, just for information """

    @property
    def identifier(self) -> Any:
        return self.processing_unit.identifier


class EOProcessorWorkFlow(EOProcessingUnit):
    """Specific EOProcessor for triggering

    It is used when the workflow is a list of processing units.
    Input EOProcessingUnits are sorted at init time to be sure that the
    execution can be done in the correct order.
    """

    def __init__(
        self,
        identifier: Any = "",
        workflow_units: Sequence[WorkFlowUnitDescription] = [],
    ) -> None:
        super().__init__(identifier)
        self.logger = EOLogging().get_logger("eopf.triggering.workflow")
        self.requested_io_outputs: dict[str, list[str]] = {}
        self.requested_io_inputs: dict[str, list[str]] = {}
        self.requested_io_adfs: dict[str, list[str]] = {}
        # reorder units
        processing_units_names = [workflow_unit.identifier for workflow_unit in workflow_units if workflow_unit.active]

        index = 0
        punits_indices = {}
        indexed_unit_workflow = {}
        for workflow_unit in workflow_units:
            punits_indices[workflow_unit.identifier] = index
            indexed_unit_workflow[index] = workflow_unit
            index += 1

        processing_units_graph = Graph(len(punits_indices))
        # create vertices of the processing_units_graph
        for workflow_unit in workflow_units:
            if not workflow_unit.active:
                break

            # create the input/output dependency graph
            for unit_input_name, input_product_id in workflow_unit.inputs.items():
                # input id is either an I/O Id or <source_process_uni>.<outputid>
                pu_id = input_product_id.split(".")[0]
                if pu_id in processing_units_names:
                    processing_units_graph.add_edge(punits_indices[workflow_unit.identifier], punits_indices[pu_id])
                else:
                    if unit_input_name in workflow_unit.processing_unit.get_mandatory_input_list(
                        **workflow_unit.parameters,
                    ):
                        self.requested_io_inputs[input_product_id] = self.requested_io_inputs.get(input_product_id, [])
                        self.requested_io_inputs.get(input_product_id, []).append(
                            f"{workflow_unit.identifier}.{unit_input_name}",
                        )
            # create the list of adfs that will be requested
            for adf_name, adf_id in workflow_unit.adfs.items():
                if adf_name in workflow_unit.processing_unit.get_mandatory_adf_list(**workflow_unit.parameters):
                    self.requested_io_adfs[adf_id] = self.requested_io_adfs.get(adf_id, [])
                    self.requested_io_adfs[adf_id].append(f"{workflow_unit.identifier}.{adf_name}")
            # create the list of outputs that will be provided
            for output_name, output_id in workflow_unit.outputs.items():
                self.requested_io_outputs[output_id] = self.requested_io_outputs.get(output_id, [])
                self.requested_io_outputs[output_id].append(f"{workflow_unit.identifier}.{output_name}")

        if processing_units_graph.has_cyclic_dependency():
            raise TriggerInvalidWorkflow("Workflow has cyclic dependencies, only acyclic allowed")
        order = processing_units_graph.topological_sort()
        self.logger.debug(f"Dependency graph : {processing_units_graph._graph}")
        self.workflow = [indexed_unit_workflow[o] for o in order]

    def run(
        self,
        inputs: MappingDataType,
        adfs: Optional[MappingAuxiliary] = None,
        **kwargs: Any,
    ) -> MappingDataType:
        """

        Parameters
        ----------
        inputs : MappingDataType
            Input dictionary
        adfs : Optional[MappingAuxiliary]
            Input ADF dictionary
        kwargs :
            Any other parameters

        Returns
        -------
         MappingDataType : Dictionary of the various internal outputs mapped to payload I/O identifier
         Output keys are constructed as:
            {unit_description.identifier}.{processing_unit_output_name}.{output_payload_io_id}

        """
        prod: dict[str, DataType | Iterable[DataType]] = {}
        available_products: dict[str, DataType | Iterable[DataType]] = dict(inputs)
        if adfs is not None:
            available_adfs: dict[str, AuxiliaryDataFile] = {adf.name: adf for adf in adfs.values()}
        else:
            available_adfs = {}
        for unit_description in self.workflow:
            if not unit_description.active:
                self.logger.info(f"{unit_description.processing_unit.identifier} is not activated")
                break

            unit_inputs = {}
            for prod_name, prod_id in unit_description.inputs.items():
                try:
                    unit_inputs[prod_name] = available_products[prod_id]
                except KeyError as e:
                    if prod_id in unit_description.processing_unit.get_mandatory_input_list(
                        **unit_description.parameters,
                    ):
                        raise TriggerInvalidWorkflow(
                            f"Missing input in pointers list : {e} for ProcessingUnit {unit_description.identifier}",
                        )
            unit_adfs = {}
            for adf_name, adf_id in unit_description.adfs.items():
                try:
                    unit_adfs[adf_name] = available_adfs[adf_id]
                except KeyError as e:
                    if adf_id in unit_description.processing_unit.get_mandatory_adf_list(**unit_description.parameters):
                        raise TriggerInvalidWorkflow(
                            f"Missing input adf in payload : {e} for ProcessingUnit {unit_description.identifier}",
                        )
            self.logger.debug(
                f"RUN {unit_description.processing_unit.identifier} with input {unit_inputs.keys()}, "
                f"adf {unit_adfs.keys()} and parameters {unit_description.parameters}",
            )

            unit_outputs = unit_description.processing_unit.run(
                inputs=unit_inputs,
                adfs=unit_adfs,
                **unit_description.parameters,
            )
            if not isinstance(unit_outputs, dict):
                raise TriggerInvalidWorkflow(f"ProcessingUnit {unit_description.identifier} is not outputting a dict")
            for output_payload_regex, output_payload_id in unit_description.outputs.items():
                matched: bool = False
                for output_name in unit_outputs.keys():
                    if re.match(output_payload_regex, output_name):
                        prod[f"{unit_description.identifier}.{output_name}.{output_payload_id}"] = unit_outputs[
                            output_name
                        ]
                        self.logger.info(
                            f"Matched {output_payload_id} with {unit_description.identifier}.{output_name}",
                        )
                        matched = True
                if not matched:
                    self.logger.warning(
                        f"{output_payload_regex} haven't match with any of {unit_description.identifier} outputs, "
                        f"available outputs : {unit_outputs.keys()}",
                    )
            for unit_output in unit_outputs.items():
                available_products[f"{unit_description.identifier}.{unit_output[0]}"] = unit_output[1]
        return MappingProxyType(prod)


class EOTriggerWorkflowParser(EOTriggeringKeyParser):
    """workflow section Parser"""

    KEY: str = "workflow"
    MANDATORY_KEYS = ("name", "module", "processing_unit")
    OPTIONAL_KEYS = ("parameters", "inputs", "outputs", "adfs", "step", "active")

    def __init__(self) -> None:
        super().__init__()
        self.LOGGER = EOLogging().get_logger()

    def _parse(
        self,
        data_to_parse: Any,
        **kwargs: Any,
    ) -> tuple[Any, list[str]]:
        errors = self.check_mandatory(data_to_parse) + self.check_unknown(data_to_parse)
        if errors:
            return None, errors
        module_name = data_to_parse.get("module")
        class_name = data_to_parse.get("processing_unit")
        processing_name = data_to_parse.get("name")
        parameters = data_to_parse.get("parameters", {}).copy()
        inputs = data_to_parse.get("inputs", {})
        outputs = data_to_parse.get("outputs", {})
        adfs = data_to_parse.get("adfs", {})
        step: int = data_to_parse.get("step", 0)
        active = data_to_parse.get("active", True)
        if active:
            try:
                module = importlib.import_module(module_name)
                try:
                    unit_class = getattr(module, class_name)
                    unit = unit_class(processing_name)
                except AttributeError:
                    return None, [f"Class {class_name} not found in module {module_name} for workflow"]
            except (
                ImportError,
                ModuleNotFoundError,
                SyntaxError,
                AttributeError,
                PermissionError,
                ValueError,
                TypeError,
                OSError,
                NameError,
            ) as e:
                return None, [f"Error while importing module {module_name} : {type(e)} {e}"]
            # verify that the input list contains the mandatory elements
            if not all(i in inputs.keys() for i in unit.get_mandatory_input_list(**parameters)):
                raise TriggerInvalidWorkflow(
                    f"Missing input for unit {module_name}.{class_name}:{processing_name}, provided {inputs.keys()} "
                    f"while requested {unit.get_mandatory_input_list(**parameters)}",
                )
            # verify that the input list contains the mandatory elements
            if not all(i in adfs.keys() for i in unit.get_mandatory_adf_list(**parameters)):
                raise TriggerInvalidWorkflow(
                    f"Missing input adf for unit {module_name}.{class_name}:{processing_name}, provided {adfs.keys()} "
                    f"while requested {unit.get_mandatory_adf_list(**parameters)}",
                )
        else:
            unit = None
        processing_unit_descr = WorkFlowUnitDescription(active, unit, inputs, adfs, outputs, parameters, step)

        return processing_unit_descr, errors

    def parse(self, data_to_parse: Union[str, dict[str, Any]], **kwargs: Any) -> Any:
        self.LOGGER.debug(f" >> {EOTriggerWorkflowParser.parse.__qualname__}")
        result = super().parse(data_to_parse, **kwargs)

        return EOProcessorWorkFlow(workflow_units=[workflow_unit for workflow_unit in result if workflow_unit.active])
