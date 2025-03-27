from typing import Optional

from kdsm_centreon_api.models.base import Model
from pydantic.fields import Field


class HostGroupConfigurationList(Model):
    id: int = Field(default=..., description="The unique identifier of the host group.")
    name: str = Field(default=..., description="The name of the host group.")
    alias: Optional[str] = Field(default=None, description="The alias of the host group.")
    notes: Optional[str] = Field(default=None, description="The notes of the host group.")
    notes_url: Optional[str] = Field(default=None, description="The notes URL of the host group.")
    action_url: Optional[str] = Field(default=None, description="The action URL of the host group.")
    icon_id: Optional[int] = Field(default=None, description="The icon ID of the host group.")
    icon_map_id: Optional[int] = Field(default=None, description="The icon map ID of the host group.")
    geo_coords: Optional[str] = Field(default=None, description="The geographical coordinates of the host group.")
    rrd: Optional[int] = Field(default=None, description="The RRD retention duration of the host group.")
    comment: Optional[str] = Field(default=None, description="The comment of the host group.")
    is_activated: bool = Field(default=..., description="The activation status of the host group.")


class HostGroupConfigurationCreate(Model):
    name: str = Field(default=..., description="The name of the host group.")
    alias: Optional[str] = Field(default=None, description="The alias of the host group.")
    notes: Optional[str] = Field(default=None, description="The notes of the host group.")
    notes_url: Optional[str] = Field(default=None, description="The notes URL of the host group.")
    action_url: Optional[str] = Field(default=None, description="The action URL of the host group.")
    icon_id: Optional[int] = Field(default=None, description="The icon ID of the host group.")
    icon_map_id: Optional[int] = Field(default=None, description="The icon map ID of the host group.")
    geo_coords: Optional[str] = Field(default=None, description="The geographical coordinates of the host group.")
    rrd: Optional[int] = Field(default=None, description="The RRD retention duration of the host group.")
    comment: Optional[str] = Field(default=None, description="The comment of the host group.")
    is_activated: Optional[bool] = Field(default=True, description="The activation status of the host group.")


class HostGroupConfigurationCreated(Model):
    id: int = Field(default=..., description="The unique identifier of the host group.")
    name: str = Field(default=..., description="The name of the host group.")
    alias: Optional[str] = Field(default=None, description="The alias of the host group.")
    notes: Optional[str] = Field(default=None, description="The notes of the host group.")
    notes_url: Optional[str] = Field(default=None, description="The notes URL of the host group.")
    action_url: Optional[str] = Field(default=None, description="The action URL of the host group.")
    icon_id: Optional[int] = Field(default=None, description="The icon ID of the host group.")
    icon_map_id: Optional[int] = Field(default=None, description="The icon map ID of the host group.")
    geo_coords: Optional[str] = Field(default=None, description="The geographical coordinates of the host group.")
    rrd: Optional[int] = Field(default=None, description="The RRD retention duration of the host group.")
    comment: Optional[str] = Field(default=None, description="The comment of the host group.")
    is_activated: bool = Field(default=..., description="The activation status of the host group.")
