import importlib
import os
import time
from abc import ABC
from collections import namedtuple
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Type, Union, cast

from xarray.core.datatree import DataTree
from zarr.errors import GroupNotFoundError

from eopf import EOConfiguration, EOContainer
from eopf.common import dtree_utils, file_utils
from eopf.common.dtree_utils import open_datatree
from eopf.common.env_utils import resolve_env_vars
from eopf.common.file_utils import AnyPath
from eopf.common.temp_utils import EOTemporaryFolder
from eopf.computing.abstract import (
    AuxiliaryDataFile,
    DataType,
    MappingAuxiliary,
    MappingDataType,
)
from eopf.daskconfig import DaskContext, init_from_eo_configuration
from eopf.daskconfig.dask_utils import is_worker_reachable
from eopf.exceptions.errors import (
    EOStoreInvalidPathError,
    MissingConfigurationParameterError,
    StoreLoadFailure,
    TriggerInvalidWorkflow,
)
from eopf.logging import EOLogging
from eopf.product.eo_product import EOProduct
from eopf.qualitycontrol.eo_qc_processor import EOQCProcessor
from eopf.store import EOProductStore
from eopf.store.zarr import EOZarrStore
from eopf.triggering.parsers.breakpoint import EOBreakPointParser
from eopf.triggering.parsers.config import EOConfigConfParser
from eopf.triggering.parsers.dask_context_parser import EODaskContextParser
from eopf.triggering.parsers.external_module_import import EOExternalModuleImportParser
from eopf.triggering.parsers.general import EOProcessParser
from eopf.triggering.parsers.general_configuration import EOGeneralConfigurationParser
from eopf.triggering.parsers.io import EOIOParser, PathType
from eopf.triggering.parsers.logging import EOLoggingConfParser
from eopf.triggering.parsers.qualitycontrol import EOQualityControlParser
from eopf.triggering.parsers.secrets import EOSecretConfParser
from eopf.triggering.parsers.workflow import (
    EOProcessorWorkFlow,
    EOTriggerWorkflowParser,
)

EOConfiguration().register_requested_parameter(
    "triggering__validate_run",
    True,
    description="validate outputs of units",
)
EOConfiguration().register_requested_parameter(
    "triggering__use_default_filename",
    True,
    description="Use default filename when using folder outputs, else use product.name",
)
EOConfiguration().register_requested_parameter(
    "triggering__use_basic_logging",
    False,
    description="Setup a basic logging",
)
EOConfiguration().register_requested_parameter(
    "triggering__load_default_logging",
    False,
    description="Load the default logging configuration from cpm",
)
EOConfiguration().register_requested_parameter(
    "triggering__wait_before_exit",
    0,
    description="Wait N seconds at end of processing to analyze dask dashboard",
)
EOConfiguration().register_requested_parameter(
    "triggering__use_datatree",
    False,
    description="Use Datatree as product type in processor unit",
)

EOConfiguration().register_requested_parameter(
    "triggering__create_temporary",
    True,
    description="Create a temporary folder at startup available in EOTemporaryFolder singleton",
)

EOConfiguration().register_requested_parameter(
    "triggering__temporary_shared",
    False,
    description="Ensure that the temporary folder is reachable from all the dask worker",
)


ParsersResults = namedtuple(
    "ParsersResults",
    [
        "breakpoints",
        "general_config",
        "processing_workflow",
        "io_config",
        "dask_context",
        "logging_config",
        "config",
        "secret_files",
        "eoqc",
    ],
)


class EORunner(ABC):
    """EORunner class implement workflow execution from a given payload"""

    def __init__(self) -> None:
        self.logger = EOLogging().get_logger("eopf.triggering.runner")

    def run_from_file(self, payload_file: Union[AnyPath, str]) -> None:
        """

        Parameters
        ----------
        payload_file : yaml payload file

        Returns
        -------
        None

        """
        payload = file_utils.load_yaml_file(payload_file)
        self.run(payload)

    def run(
        self,
        payload: dict[str, Any],
    ) -> None:
        """Generic method that apply the algorithm of the processing unit
        from the payload and write the result product.

        Parameters
        ----------
        payload: dict[str, Any]
            dict of metadata to find and run the processing unit, create the output product
            and write it.
        """

        self.logger.debug(f" >> {EORunner.run.__qualname__}")
        parsers_results = self.extract_from_payload_and_init_conf_logging(payload)
        # Temporary dictionary ?
        if EOConfiguration().get("triggering__create_temporary", True):
            temp_dir = EOTemporaryFolder().get()
            if EOConfiguration().get("triggering__temporary_shared", False):
                if not is_worker_reachable(temp_dir):
                    raise TriggerInvalidWorkflow(f"Temporary folder {temp_dir} is not reachable from the workers !!!!")
        # If datatree option then deactivate validation
        if bool(EOConfiguration().triggering__use_datatree):
            self.logger.info("Datatree mode activated, deactivating validation")
            EOConfiguration().load_dict({"triggering": {"validate_run": False}})
        # Dask instance
        if parsers_results.dask_context is None:
            self.logger.info("No Dask context provided in payload, using EOConfiguration")
            dask_context = init_from_eo_configuration()
        else:
            dask_context = parsers_results.dask_context
        # i/o config
        inputs_io_products = {p["id"]: p for p in parsers_results.io_config["input_products"]}
        inputs_io_adfs = {p["id"]: p for p in parsers_results.io_config["adfs"]}
        output_io_products = {p["id"]: p for p in parsers_results.io_config["output_products"]}
        # Validate the workflow
        self.validate_workflow(
            inputs_io_adfs,
            inputs_io_products,
            output_io_products,
            parsers_results.processing_workflow,
        )

        # Instanciate EOQCProcessor
        if parsers_results.eoqc is not None:
            self.logger.debug("Instanciating EOQCProcessor")
            _eoqc_processor: EOQCProcessor = EOQCProcessor(
                config_folder=parsers_results.eoqc.get("config_folder", "default"),
                parameters=parsers_results.eoqc.get("parameters"),
                update_attrs=parsers_results.eoqc.get("update_attrs", True),
                report_path=parsers_results.eoqc.get("report_path"),
                config_path=parsers_results.eoqc.get("config_path"),
                additional_config_folders=parsers_results.eoqc.get("additional_config_folders"),
            )
        else:
            _eoqc_processor = EOQCProcessor()

        with dask_context:
            if dask_context is not None:
                self.logger.info(f"Dask context : {dask_context}")
            # Open input products
            io_opened_products: Mapping[str, DataType | Iterable[DataType]] = self.open_input_products(
                inputs_io_products,
                parsers_results.processing_workflow,
            )
            # List ADFs
            io_interpreted_adf = self.list_input_adfs(inputs_io_adfs, parsers_results.processing_workflow)
            # Run the workflow
            outputs = self.run_workflow(io_interpreted_adf, io_opened_products, parsers_results.processing_workflow)
            # Write results
            self.write_outputs(output_io_products, outputs, _eoqc_processor)
            # End of computation part
            self.logger.info("Computation finished and output products written !")
            # Wait to let the user check the local dask dashboard
            self.logger.info(f"Sleeping for {EOConfiguration().triggering__wait_before_exit}s")
            if isinstance(dask_context, DaskContext) and dask_context.client is not None:
                self.logger.info(f"Dask dashboard can be reached at : {dask_context.client.dashboard_link}")
            time.sleep(EOConfiguration().triggering__wait_before_exit)

    def write_outputs(
        self,
        output_io_products: dict[str, Any],
        outputs: MappingDataType,
        eoqc_processor: EOQCProcessor,
    ) -> None:
        """
        Write outputs defined in workflow
        Parameters
        ----------
        eoqc_processor
        output_io_products : payload output descriptors
        outputs: MappingDataType
        eoqc_processor: EOQCProcessor,

        Output keys are constructed as i workflow::

            {unit_description.identifier}.{processing_unit_output_name}.{output_payload_io_id}

        Returns
        -------
        None
        """
        self.logger.info(f"Starting outputs gathering {outputs.keys()}")
        already_used_output_payload_io_id = []

        for output_unit_id, data in outputs.items():
            self.logger.info(f"id : {output_unit_id}")
            self.logger.info(f"data: {data}")
            output_payload_io_id: str
            pu_identifier, processing_unit_output_name, output_payload_io_id = output_unit_id.split(".")
            try:
                output_io_param = output_io_products[output_payload_io_id]
            except KeyError as e:
                raise TriggerInvalidWorkflow(f"Missing output : {e} in I/O definitions")
            # Can't reuse twice a non folder output
            if output_payload_io_id in already_used_output_payload_io_id and output_io_param["type"] != PathType.Folder:
                raise TriggerInvalidWorkflow(f"Multiple reuse of a non folder output io id : {output_payload_io_id}")
            store = output_io_param["store_class"]
            storage_options = output_io_param["store_params"]
            if not isinstance(data, (EOProduct, EOContainer, DataTree)):
                self.logger.info(f"Iterable {data}")
                for eo_data in data:
                    if isinstance(eo_data, (EOProduct, EOContainer, DataTree)):
                        self._write_single_output(eo_data, eoqc_processor, output_io_param, storage_options, store)
            else:
                self._write_single_output(data, eoqc_processor, output_io_param, storage_options, store)
            already_used_output_payload_io_id.append(output_payload_io_id)

    def _write_single_output(
        self,
        eo_data: DataType,
        eoqc_processor: EOQCProcessor,
        output_io_param: dict[str, Any],
        storage_options: dict[str, Any],
        store: Type[EOProductStore],
    ) -> None:
        self.logger.info(f"In single product write {output_io_param}")
        if bool(EOConfiguration().triggering__use_datatree):
            if isinstance(eo_data, DataTree):
                if store == EOZarrStore:
                    if output_io_param["type"] == PathType.Folder:
                        if EOConfiguration().triggering__use_default_filename:
                            product_name = dtree_utils.get_default_file_name_datatree(eo_data)
                        else:
                            product_name = eo_data.name if eo_data.name is not None else ""
                        dirpath_anypath: AnyPath = output_io_param["path"]
                    else:
                        dirpath_anypath = output_io_param["path"].dirname()
                        product_name = output_io_param["path"].basename
                    if not dirpath_anypath.exists():
                        dirpath_anypath.mkdir()

                    self.logger.info(
                        f"Writing Datatree {product_name} to {dirpath_anypath}/{product_name} "
                        f"with params {storage_options}",
                    )
                    dtree_utils.write_datatree(
                        eo_data,
                        dirpath_anypath / product_name,
                        mode=output_io_param["opening_mode"].value.file_opening_mode,
                        **storage_options,
                    )
                    return
                else:
                    eo_product = EOProduct.from_datatree(eo_data)
            else:
                self.logger.warning(
                    "Output product is not a DataTree, product will not be written with xarray.",
                )
                self.logger.warning(
                    f"Product type: {type(eo_data)}",
                )
                eo_product = cast(EOProduct, eo_data)
        else:
            eo_product = cast(EOProduct, eo_data)
        if output_io_param["type"] == PathType.Folder:
            if EOConfiguration().triggering__use_default_filename:
                product_name = ""
            else:
                product_name = eo_product.name if eo_product.name is not None else ""
            dirpath_anypath = output_io_param["path"]
        else:
            dirpath_anypath = output_io_param["path"].dirname()
            product_name = output_io_param["path"].basename
        if not dirpath_anypath.exists():
            dirpath_anypath.mkdir()
        output_store = store(url=dirpath_anypath).open(mode=output_io_param["opening_mode"], **storage_options)
        # This will write the product
        self.logger.info(
            f"Writing eoproduct {product_name} to {dirpath_anypath}/{product_name} " f"with params {storage_options}",
        )
        if EOConfiguration().has_value("dask__export_graphs"):
            folder = AnyPath.cast(EOConfiguration().dask__export_graphs)
            self.logger.info(f"EOVariables Dask graphs export requested in {folder}")
            folder.mkdir(exist_ok=True)
            eo_product.export_dask_graph(folder)
        # Apply qualitycontrol if requested
        if output_io_param["apply_eoqc"] and isinstance(eo_product, EOProduct):
            eoqc_processor.check(eo_product)
        # Effectively write it down
        output_store[product_name] = eo_product

    @staticmethod
    def run_workflow(
        io_interpreted_adf: MappingAuxiliary,
        io_opened_products: MappingDataType,
        processing_workflow: EOProcessorWorkFlow,
    ) -> MappingDataType:
        logger = EOLogging().get_logger("eopf.triggering.runner")
        if EOConfiguration().triggering__validate_run:
            logger.info("Starting workflow run_validating")
            outputs: MappingDataType = processing_workflow.run_validating(
                inputs=io_opened_products,
                adfs=io_interpreted_adf,
            )
        else:
            logger.info("Starting workflow run")
            outputs = processing_workflow.run(inputs=io_opened_products, adfs=io_interpreted_adf)

        return outputs

    def list_input_adfs(
        self,
        inputs_io_adfs: dict[str, Any],
        processing_workflow: EOProcessorWorkFlow,
    ) -> dict[str, AuxiliaryDataFile]:
        """
        Convert ADF definition from TT to ADF structures
        Parameters
        ----------
        processing_workflow
        inputs_io_adfs

        Returns
        -------
        io_interpreted_adf
        """
        io_interpreted_adf: dict[str, AuxiliaryDataFile] = {}
        for adf in inputs_io_adfs.values():
            adf_id = adf["id"]
            new_adf = AuxiliaryDataFile(name=adf_id, path=adf["path"], store_params=adf["store_params"])
            if not new_adf.path.exists() and adf_id in processing_workflow.requested_io_adfs:
                raise TriggerInvalidWorkflow(
                    f"{adf_id} adf is requested for {processing_workflow.requested_io_adfs[adf_id]}"
                    f" but is not able to open it",
                )
            io_interpreted_adf[adf_id] = new_adf
            self.logger.info(f"Adding ADF : {new_adf}")
        return io_interpreted_adf

    def open_input_products(
        self,
        inputs_io_products: Mapping[str, Any],
        processing_workflow: EOProcessorWorkFlow,
    ) -> MappingDataType:
        """
        Open the input products defined in the TT
        Parameters
        ----------
        processing_workflow
        inputs_io_products : TT products infos

        Returns
        -------
        input products mapping
        """
        io_opened_products: dict[str, DataType | Iterable[DataType]] = {}
        for input_product in inputs_io_products.values():
            self.logger.info(f"Opening product : {input_product}")
            input_product_anypath: AnyPath = input_product["path"]
            self.logger.debug(f"{input_product_anypath.__repr__()}")
            product_id = input_product["id"]
            input_type = input_product["type"]
            product_path_list = [input_product_anypath]
            if input_type == PathType.Regex:
                if "regex" not in input_product["store_params"]:
                    raise KeyError("missing regex param in store_params for regex selection")
                product_path_list = input_product_anypath.glob(input_product["store_params"]["regex"])
                if "multiplicity" in input_product["store_params"]:
                    if input_product["store_params"]["multiplicity"] == "exactly_one":
                        if len(product_path_list) != 1:
                            raise TriggerInvalidWorkflow(
                                f"Requested a single product for {product_id}, found {len(product_path_list)}",
                            )
                    elif input_product["store_params"]["multiplicity"] == "at_least_one":
                        if len(product_path_list) == 0:
                            raise TriggerInvalidWorkflow(f"Requested at least one product for {product_id}, found 0")
                    elif input_product["store_params"]["multiplicity"] == "more_than_one":
                        if len(product_path_list) < 2:
                            raise TriggerInvalidWorkflow(
                                f"Requested more than one product for {product_id}, found {len(product_path_list)}",
                            )
                    elif input_product["store_params"]["multiplicity"].isdigit():
                        number_of_res = int(input_product["store_params"]["multiplicity"])
                        if len(product_path_list) < number_of_res:
                            raise TriggerInvalidWorkflow(
                                f"Requested at least {number_of_res} product for {product_id},"
                                f" found {len(product_path_list)}",
                            )
                    else:
                        raise TriggerInvalidWorkflow(
                            "Unknown multiplicity value : exactly_one, at_least_one,"
                            " more_than_one or a digit requested",
                        )
            elif input_type == PathType.Folder:
                product_path_list = input_product_anypath.ls()
            try:
                if len(product_path_list) == 0:
                    raise TriggerInvalidWorkflow(f"No product found for : {input_product} !!!!")
                if len(product_path_list) > 1:
                    io_opened_products[product_id] = []
                    for p in product_path_list:
                        product = self._open_input_product(input_product, p, product_id)
                        # Ignore type as it seems mypy doesn't detect that it is a list
                        io_opened_products[product_id].append(product)  # type: ignore
                else:
                    self.logger.info(f"Opening {product_path_list}")
                    io_opened_products[product_id] = self._open_input_product(
                        input_product,
                        product_path_list[0],
                        product_id,
                    )
            except (StoreLoadFailure, EOStoreInvalidPathError, TriggerInvalidWorkflow, GroupNotFoundError) as err:
                if product_id in processing_workflow.requested_io_inputs:
                    raise TriggerInvalidWorkflow(
                        f"{product_id} input is requested for {processing_workflow.requested_io_inputs[product_id]}"
                        f" but is not able to open it",
                    ) from err
        return MappingProxyType(io_opened_products)

    def _open_input_product(
        self,
        input_product: dict[str, Any],
        input_produt_anypath: AnyPath,
        product_id: str,
    ) -> DataType:
        # DataTree prevails in case of zarr store and datatree activated
        self.logger.info(f"Input read : {bool(EOConfiguration().triggering__use_datatree)}")
        if bool(EOConfiguration().triggering__use_datatree):
            if input_product["store_class"] == EOZarrStore:
                product: DataType = open_datatree(input_produt_anypath, product_id)
            else:
                tmp_product: EOProduct = input_product["store_class"](url=input_produt_anypath).load(
                    product_id,
                )
                product = tmp_product.to_datatree()
        else:
            product = input_product["store_class"](url=input_produt_anypath).load(input_product["id"])
        return product

    def validate_workflow(
        self,
        inputs_io_adfs: Mapping[str, Any],
        inputs_io_products: Mapping[str, Any],
        output_io_products: Mapping[str, Any],
        processing_workflow: EOProcessorWorkFlow,
    ) -> None:
        """
        Validate that the workflow is ok to be run, if not raise TriggerInvalidWorkFlow
        Parameters
        ----------
        inputs_io_adfs
        inputs_io_products
        output_io_products
        processing_workflow

        Returns
        -------
        None

        Raises
        ------
        TriggerInvalidWorkflow
        """
        # Do some verification
        for requested_input, units_requesting in processing_workflow.requested_io_inputs.items():
            if requested_input not in inputs_io_products:
                raise TriggerInvalidWorkflow(
                    f"{requested_input} input is requested for {units_requesting}"
                    f" but is not available in I/O configuration",
                )
        for requested_adf, units_requesting in processing_workflow.requested_io_adfs.items():
            if requested_adf not in inputs_io_adfs:
                raise TriggerInvalidWorkflow(
                    f"{requested_adf} adf input is requested for {units_requesting}"
                    f" but is not available in I/O adf configuration",
                )
        for requested_output, units_requesting in processing_workflow.requested_io_outputs.items():
            if requested_output not in output_io_products:
                raise TriggerInvalidWorkflow(
                    f"{requested_output} output is requested for {units_requesting}"
                    f" but is not available in I/O configuration",
                )
            if len(units_requesting) > 1 and output_io_products[requested_output]["type"] != PathType.Folder:
                raise TriggerInvalidWorkflow(
                    f"{requested_output} output is requested multiple times for {units_requesting}"
                    f" but is not a folder type",
                )
        # verify conf
        try:
            EOConfiguration().validate_mandatory_parameters(throws=True)
        except MissingConfigurationParameterError as e:
            raise TriggerInvalidWorkflow("Missing EOConfiguration params to run the TaskTable") from e

    def extract_from_payload_and_init_conf_logging(
        self,
        payload: dict[str, Any],
    ) -> ParsersResults:
        """Retrieve all the information from the given payload

        the payload should have this keys:

            * 'workflow': describe the processing workflow to run
            * 'breakpoints': configure workflow element as breakpoint
            * 'I/O': configure Input/Output element
            * 'dask_context': configure dask scheduler and execution
            * 'logging': configure logging ( optional)
            * 'config' : configure all (optional)

        See :ref:`triggering-usage`

        Parameters
        ----------
        payload: dict[str, Any]

        Returns
        -------
        tuple:
            All component corresponding to the metadata
        """
        # resolve all env_vars in the payload
        payload = resolve_env_vars(payload)
        EOConfiguration().clear_loaded_configurations()

        # first load the config
        result = EOProcessParser(EOConfigConfParser).parse(payload)
        config = result["config"]
        # register the provided configuration files
        for conf in config:
            EOConfiguration().load_file(conf)
        # secrets
        result = EOProcessParser(EOSecretConfParser).parse(payload)
        secret_files = result["secret"]
        # register the provided secret files
        for sec in secret_files:
            EOConfiguration().load_secret_file(sec)
        # load the general config
        result = EOProcessParser(EOGeneralConfigurationParser).parse(payload)
        general_config = result["general_configuration"]
        for d in general_config:
            # register the dict
            EOConfiguration().load_dict(d)

        # basic config ?
        if EOConfiguration().get("triggering__use_basic_logging", False):
            EOLogging.setup_basic_config()
        # then load the logging
        result = EOProcessParser(EOLoggingConfParser).parse(payload)
        logging_config = result["logging"]
        if EOConfiguration().get("triggering__load_default_logging", default=False):
            EOLogging().enable_default_conf()
        # register the provided logging_config
        for log_conf in logging_config:
            EOLogging().register_cfg(os.path.splitext(os.path.basename(log_conf))[0], log_conf)
        # Additional imports
        additional_imported_modules = EOProcessParser(EOExternalModuleImportParser).parse(payload)["external_modules"]
        self.import_external_modules(additional_imported_modules)
        # Breakpoint activation
        result = EOProcessParser(EOBreakPointParser).parse(payload)
        breakpoints = result["breakpoints"]
        self.activate_breakpoints(breakpoints)
        # Load the other elements ( breakpoints, workflow, I/O)
        parsers = (
            EOTriggerWorkflowParser,
            EOIOParser,
            EODaskContextParser,
            EOQualityControlParser,
        )
        result = EOProcessParser(*parsers).parse(payload)
        # Worflow stuff
        dask_context = result["dask_context"]
        io_config = result["I/O"]
        processing_workflow = result["workflow"]
        eoqc = result["eoqc"]

        return ParsersResults(
            breakpoints=breakpoints,
            general_config=general_config,
            processing_workflow=processing_workflow,
            io_config=io_config,
            dask_context=dask_context,
            logging_config=logging_config,
            config=config,
            secret_files=secret_files,
            eoqc=eoqc,
        )

    def activate_breakpoints(self, io_breakpoint: dict[str, Any]) -> None:
        """
        Activate the corresponding breakpoints. If all or ALL in the list activate ALL breakpoints in the code
        Parameters
        ----------
        io_breakpoint : breakpoints data coming from parser

        Returns
        -------

        """
        if len(io_breakpoint) == 0:
            return

        if io_breakpoint["all"]:
            EOConfiguration()["breakpoints__activate_all"] = True
            return
        for brkp in io_breakpoint["ids"]:
            EOConfiguration()[f"breakpoints__{brkp}"] = True
        if io_breakpoint["folder"] is not None:
            EOConfiguration()["breakpoints__folder"] = io_breakpoint["folder"]
        if io_breakpoint["store_params"] is not None:
            EOConfiguration()["breakpoints__storage_options"] = io_breakpoint["store_params"]

    def import_external_modules(self, module_list: list[dict[str, str]]) -> None:
        """
        Import external modules
        Parameters
        ----------
        module_list : list of modules to load

        Returns
        -------

        """
        global_dict = globals()
        for module in module_list:
            try:
                # Determine the name to use in the global namespace
                module_name_in_globals = module["alias"] if module["alias"] else module["name"]
                module_name = module["name"]
                imported_module = importlib.import_module(module_name)
                global_dict[module_name_in_globals] = imported_module
                self.logger.info(f"Module {module_name} loaded successfully as {module_name_in_globals}")
                if module["nested"]:
                    # Optionally, you can also inject specific attributes of the module
                    for attribute_name in dir(imported_module):
                        # don't load private attr
                        if not attribute_name.startswith("_"):
                            global_dict[attribute_name] = getattr(imported_module, attribute_name)
            except ModuleNotFoundError as err:
                raise TriggerInvalidWorkflow(f"Module {module_name} not found") from err
