from typing import Optional

from kdsm_centreon_api.models.base import Model
from pydantic.fields import Field


class ServiceGroupConfigurationList(Model):
    id: int = Field(default=..., description="The unique identifier of the service group.")
    name: str = Field(default=..., description="The name of the service group.")
    alias: Optional[str] = Field(default=None, description="The alias of the service group.")
    geo_coords: Optional[str] = Field(default=None, description="The geographical coordinates of the service group.")
    comment: Optional[str] = Field(default=None, description="The comment of the service group.")
    is_activated: bool = Field(default=..., description="The activation status of the service group.")
