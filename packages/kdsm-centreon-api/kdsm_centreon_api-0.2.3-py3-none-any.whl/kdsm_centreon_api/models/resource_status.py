from enum import Enum

from kdsm_centreon_api.models.base import Model
from pydantic import Field


class ResourceStatusName(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    UNREACHABLE = "UNREACHABLE"
    PENDING = "PENDING"
    OK = "OK"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"


class ResourceStatus(Model):
    code: int = Field(default=..., ge=0, le=4, description="The status code of the resource.")
    name: ResourceStatusName = Field(default=..., description="The status name of the resource.")
    severity_code: int = Field(default=..., ge=0, le=5, description="The severity code of the resource.")
