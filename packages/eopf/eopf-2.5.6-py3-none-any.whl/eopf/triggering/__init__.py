"""The eopf.triggering module simplifies the integration of processing units
with the most widespread processing orchestration systems
(Spring Cloud Data Flow, Apache Airflow, Zeebee, Apache Beam ...).
"""

from eopf.triggering.runner import EORunner

__all__ = ["EORunner"]
