from typing import Optional

from kdsm_centreon_api.models.base import Model
from pydantic.fields import Field


class MonitoringServerList(Model):
    id: int = Field(default=..., description="The unique identifier of the monitoring server.")
    name: str = Field(default=..., description="The name of the monitoring server.")
    address: str = Field(default=..., description="The address of the monitoring server.")
    is_localhost: bool = Field(default=..., description="Indicates whether the monitoring server is the localhost or not.")
    is_default: bool = Field(default=..., description="Indicates whether the monitoring server is the default or not.")
    ssh_port: int = Field(default=..., description="The SSH port of the monitoring server.")
    last_restart: Optional[str] = Field(default=None, description="The last restart of the monitoring server.")
    engine_start_command: str = Field(default=..., description="The engine start command of the monitoring server.")
    engine_stop_command: str = Field(default=..., description="The engine stop command of the monitoring server.")
    engine_restart_command: str = Field(default=..., description="The engine restart command of the monitoring server.")
    engine_reload_command: str = Field(default=..., description="The engine reload command of the monitoring server.")
    nagios_bin: str = Field(default=..., description="The Nagios binary of the monitoring server.")
    nagiostats_bin: str = Field(default=..., description="The Nagios stats binary of the monitoring server.")
    centreonbroker_cfg_path: str = Field(default=..., description="The Centreon Broker configuration path of the monitoring server.")
    centreonbroker_module_path: str = Field(default=..., description="The Centreon Broker module path of the monitoring server.")
    centreonbroker_logs_path: Optional[str] = Field(default=None, description="The Centreon Broker logs path of the monitoring server.")
    centreonconnector_path: str = Field(default=..., description="The Centreon Connector path of the monitoring server.")
    init_script_centreontrapd: str = Field(default=..., description="The init script Centreon Trapd of the monitoring server.")
    snmp_trapd_path_conf: str = Field(default=..., description="The SNMP Trapd path configuration of the monitoring server.")
    is_updated: bool = Field(default=..., description="Indicates whether the monitoring server is updated or not.")
    is_activate: bool = Field(default=..., description="Indicates whether the monitoring server is activated or not.")
