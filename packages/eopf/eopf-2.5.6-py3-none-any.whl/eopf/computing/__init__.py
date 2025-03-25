"""eopf.computing module provide to re-engineered processor developers a
homogeneous API implementing advanced parallelism features whatever the execution context: HPC, Cloud or local.
"""

from eopf.computing.abstract import (
    ADF,
    AuxiliaryDataFile,
    EOProcessingStep,
    EOProcessingUnit,
)
from eopf.computing.breakpoint import declare_as_breakpoint, eopf_breakpoint_decorator
from eopf.computing.overlap import map_overlap

__all__ = [
    "EOProcessingStep",
    "EOProcessingUnit",
    "AuxiliaryDataFile",
    "ADF",
    "eopf_breakpoint_decorator",
    "declare_as_breakpoint",
    "map_overlap",
]
