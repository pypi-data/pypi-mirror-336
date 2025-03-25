import logging.config
from typing import TYPE_CHECKING, Any

import dask.config
from distributed.config import initialize_logging

from eopf import EOLogging

if TYPE_CHECKING:  # pragma: no cover
    from distributed.client import Client

DEFAULT_FMT: str = (
    "%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(lineno)d : "
    "(Process Details : (%(process)d, %(processName)s), "
    "Thread Details : (%(thread)d, %(threadName)s))\nLog : %(message)s"
)


def configure_dask_logging(cluster_type: Any, logging_config: dict[str, Any], default_fmt: str = DEFAULT_FMT) -> None:
    if cluster_type is not None:
        distributed_config = {"distributed": {"logging": logging_config}}
        if "version" not in logging_config:
            distributed_config["distributed"].setdefault("admin", {})["log-format"] = logging_config.pop(
                "distributed.admin.log-format",
                default_fmt,
            )
        dask.config.set({"distributed.logging": logging_config})
        initialize_logging(distributed_config)
    else:
        logging.config.dictConfig(logging_config)


def print_dask_client_cluster_info(client: "Client") -> None:
    logger = EOLogging().get_logger("eopf.dask_utils")
    if client is not None:
        # If a client exists, print information about the scheduler and workers
        scheduler_info = client.scheduler_info()
        logger.info("Dask Cluster Information:")
        logger.info("=========================")
        logger.info("Scheduler:")
        logger.info(scheduler_info["address"])

        for worker, worker_info in scheduler_info["workers"].items():
            logger.info("Worker:", worker)
            logger.info("  - Address:", worker_info["address"])
            logger.info("  - Memory:", worker_info["memory"])
            logger.info("  - CPUs:", worker_info["nthreads"])
            logger.info("  - Processes:", worker_info["nprocesses"])
            logger.info("  - GPU Info:", worker_info["gpu"])
