from kdsm_centreon_api.models.base import Model
from pydantic.fields import Field


class MonitoringServerMin(Model):
    id: int = Field(default=..., description="The unique identifier of the monitoring server.")
    name: str = Field(default=..., description="The name of the monitoring server.")


class TimeperiodMin(Model):
    id: int = Field(default=..., description="The unique identifier of the timeperiod.")
    name: str = Field(default=..., description="The name of the timeperiod.")


class SeverityMin(Model):
    id: int = Field(default=..., description="The unique identifier of the severity.")
    name: str = Field(default=..., description="The name of the severity.")


class HostTemplateMin(Model):
    id: int = Field(default=..., description="The unique identifier of the host template.")
    name: str = Field(default=..., description="The name of the host template.")


class HostMin(Model):
    id: int = Field(default=..., description="The unique identifier of the host.")
    name: str = Field(default=..., description="The name of the host.")


class HostRtmMin(Model):
    id: int = Field(default=..., description="The unique identifier of the host.")
    alias: str = Field(default=..., description="The alias of the host.")
    display_name: str = Field(default=..., description="The display name of the host.")
    name: str = Field(default=..., description="The name of the host.")
    state: str = Field(default=..., le=0, ge=4, description="The state of the host.")


class HostGroupMin(Model):
    id: int = Field(default=..., description="The unique identifier of the host group.")
    name: str = Field(default=..., description="The name of the host group.")


class ServiceTemplateMin(Model):
    id: int = Field(default=..., description="The unique identifier of the service template.")
    name: str = Field(default=..., description="The name of the service template.")


class ServiceGroupMin(Model):
    id: int = Field(default=..., description="The unique identifier of the service group.")
    name: str = Field(default=..., description="The name of the service group.")


class ServiceRtmMin(Model):
    id: int = Field(default=..., description="The unique identifier of the service.")
    description: str = Field(default=..., description="The description of the service.")
    display_name: str = Field(default=..., description="The display name of the service.")
    state: str = Field(default=..., le=0, ge=4, description="The state of the service.")
