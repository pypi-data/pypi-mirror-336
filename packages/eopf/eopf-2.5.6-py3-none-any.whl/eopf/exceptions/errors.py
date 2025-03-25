"""

General exceptions

"""


class MissingArgumentError(Exception):
    """Raised when missing an argument on a function call"""


class EOConfigurationError(Exception):
    """Parent class of all configuration errors"""


class MissingConfigurationParameterError(Exception):
    """Raised when object configuration is not register_requested_parameter"""


class InvalidConfigurationError(Exception):
    """Raised when object configuration is not register_requested_parameter"""


class NetcdfIncompatibilityError(Exception):
    """Raised when a request is incompatible with the netcdf format or library"""


class XmlParsingError(Exception):
    """Raised when xml has a non-expected structure"""


class XmlXpathError(Exception):
    """Raised when an error occurs on an XPath query"""


class JSONParsingError(Exception):
    """Raised when json have a non-valid structure"""


class FormattingError(Exception):
    """When a formatter raises exceptions"""


class FormattingDecoratorMissingUri(Exception):
    """When the decorated function is missing an argument path, url or key"""


class XmlManifestNetCDFError(Exception):
    """When trying to compile the manifest from NetCDF data (Sentinel-3)"""


class DaskProfilerError(Exception):
    """When the dask_profiler raises any error"""


class DaskClusterNotFound(Exception):
    """When the dask gateway cluster requested is not available"""


class SingleThreadProfilerError(Exception):
    """When the single_thread_profiler raises any error"""


class EOPathError(Exception):
    """Raised by any eopath problem"""


class ProductRetrievalError(Exception):
    """Raised when a legacy product can not be retrieved"""


# EOProduct exceptions


class EOProductError(Exception):
    """Parent class of product Exception"""


class EOGroupExistError(EOProductError):
    """Raised by EOGroup when one redefines an existing key"""


class EOGroupResolutionError(EOProductError):
    """Raised by EOGroup in case of resolution problem"""


class EOGroupInvalidRequestError(EOProductError):
    """When a bad request has been done in eogroup"""


class EOGroupReadError(EOProductError):
    """Raised when group can not be read from disk"""


class EOVariableReadError(EOProductError):
    """Raised when variable can not be read from disk"""


class EOVariableSubSetError(EOProductError):
    """Raised by EOVariable when an error occurs in subsetting"""


class EOVariableInvalidDimensionsError(EOProductError):
    """Raised when an invalid dimension is detected"""


class EOVariableAssignCoordsError(EOProductError):
    """Raised when a coordinate could not be assigned to an EOVariable"""


class EOObjectMultipleParentError(EOProductError):
    """Raised by `EOObject` with already register_requested_parameter parent and
    manipulated in context with an other parent"""


class InvalidProductError(EOProductError):
    """Raised when trying to manipulate a product without valid requirement"""


class ProductNotLoaded(EOProductError):
    """Raised when compute is called on an EOProduct that is not loaded"""


class ProductAlreadyOpened(EOProductError):
    """Raised when opening an already opened product"""


"""
Store Exceptions
"""


class EOContainerError(Exception):
    """Parent class of EOContainer Exception"""


class EOContainerSetitemError(Exception):
    """Parent class of EOContainer Exception"""


"""
Store Exceptions
"""


class EOStoreException(Exception):
    """Parent exception for all store exceptions"""


class EOStoreInvalidRequestError(EOStoreException):
    """When a bad request has been done in an eostore"""


class EOStoreAlreadyOpenRequestError(EOStoreException):
    """When opening an already opened eostore"""


class EOStoreInvalidPathError(EOStoreException):
    """When a wrong path has been register_requested_parameter in an eostore"""


class EOStoreProductAlreadyExistsError(EOStoreException):
    """When creating an already existing eostore"""


class MappingAccessorNotFoundError(EOStoreException):
    """Raised when the corresponding accessor is not found"""


class MappingConfigurationError(EOStoreException):
    """Raised when an error occurs while retrieving an accessor config from the mapping"""


class TemplateMissingError(EOStoreException):
    """Raised when no template has been found for a product type"""


class EOSafeStoreInvalidPathError(EOStoreException):
    """Raised when a requested path does not exist in the store"""


class EOCogStoreInvalidPathError(EOStoreException):
    """Raise when an invalid path to a group/variable is requested"""


class EOStoreFactoryNoRegisteredStoreError(EOStoreException):
    """Raised when no store can be provided"""


class StoreNotDefinedError(EOStoreException):
    """Raised when store is None in the given context"""


class StoreNotOpenError(EOStoreException):
    """Raised when trying to access a closed store"""


class StoreMissingAttr(EOStoreException):
    """Raised when a store does not have defined an attribute"""


class StoreInvalidMode(EOStoreException):
    """Raised when opening a store in an invalid mode"""


class StoreOpenFailure(EOStoreException):
    """Raised when a store fails to open"""


class StoreLoadFailure(EOStoreException):
    """Raised when a store fails to load an EOProduct"""


class StoreWriteFailure(EOStoreException):
    """Raised when a store fails to write an EOProduct"""


class StoreReadFailure(EOStoreException):
    """Raised when a product can not be read by Store"""


class RecognitionFunctionNotDefinedError(EOStoreException):
    """Raised when a product can not be read by Store"""


"""
Accessors exceptions
"""


class AccessorError(Exception):
    """Parent exception on all accessor exceptions"""


class AccessorNotDefinedError(AccessorError):
    """Raised when accessor is None in the given context"""


class AccessorNotOpenError(AccessorError):
    """Raised when trying to access a closed accessor"""


class AccessorInvalidRequestError(AccessorError):
    """Raised when an invalid request is done on an accessor, for example with a non-existing path"""


class AccessorInvalidPathError(EOStoreException):
    """When a wrong path has been register_requested_parameter in an eoaccessor"""


class AccessorRetrieveError(AccessorError):
    """Raised when retrieval of data via the accessor is failing"""


class AccessorInvalidMode(AccessorError):
    """Raised when opening an accessor in an invalid mode"""


class AccessorInvalidMappingParameters(AccessorError):
    """Raised when parameters from mapping are invalid"""


class AccessorInitError(AccessorError):
    """Raised when an accessor can not be initialised"""


class AccessorOpenError(AccessorError):
    """Raised when an accessor can not be opened"""


"""
Logging Exceptions
"""


class LoggingError(Exception):
    """Parent exception for all logging exceptions"""


class LoggingConfigurationDirDoesNotExist(LoggingError):
    """When the preset or given logging directory does not exist"""


class LoggingConfigurationFileTypeNotSupported(LoggingError):
    """When the logging file name does not have a .conf or .yaml extension"""


class LoggingConfigurationNotRegistered(LoggingError):
    """When a given logging configuration name is not registered"""


class LoggingConfigurationFileIsNotValid(LoggingError):
    """When a given logging configuration file .conf/.yaml cannot be applied"""


class LoggingDictConfigurationInvalid(LoggingError):
    """Raised when the logging configuration given as dict is not valid"""


"""
QualityControl Exceptions

"""


class EOQCError(Exception):
    """Parent class of Quality Control Exceptions"""


class EOQCInspectionError(Exception):
    """When an inspection raised an exception"""


class EOQCConfigMissing(EOQCError):
    """When there is no default configuration for the given product type"""


class EOQCConfigMalformed(EOQCError):
    """When there is no default configuration for the given product type"""


class EOQCInspectionMissing(EOQCError):
    """When there is no default configuration for the given product type"""


class EOQCInspectionMalformed(EOQCError):
    """When there is no default configuration for the given product type"""


"""
Triggering Exceptions

"""


class TriggeringError(Exception):
    """Parent class of Triggering Exceptions"""


class TriggeringConfigurationError(TriggeringError):
    """When triggering configuration file is wrong"""


class TriggeringInternalError(TriggeringError):
    """Raised when a triggering internal error occurs"""


class TriggerInvalidWorkflow(TriggeringError):
    """Raised when an error occurs in the workflow"""


"""
Tracing Exceptions
"""


class TracingError(Exception):
    """Parent class of Triggering Exceptions"""


class ProgressConfigurationError(TracingError):
    """When progress configuration is not register_requested_parameter"""


class ProgressStepProgress(TracingError):
    """When the sum of each progress step is not sum_max_progress"""


class MaskingError(TracingError):
    """When an error occurs during the masking of an EOVariable"""


class ScalingError(TracingError):
    """When an error occurs during the scaling of an EOVariable"""


# MappingFormatter errors
class MappingFormatterError(Exception):
    """Base MappingFormatter error"""


class MissingArgumentsMappingFormatterError(Exception):
    """Raised when arguments are missing for a specific Mapping Formatter"""


class MappingDefinitionError(Exception):
    """When elements of a mapping are not correctly defined or missing"""


# MappingFactory errors
class EOPFMappingFactory(Exception):
    """Base EOPFMappingFactory error"""


class MappingRegistrationError(EOPFMappingFactory):
    """When registration of mappings fails"""


class MappingMissingError(EOPFMappingFactory):
    """When no mapping is found"""
