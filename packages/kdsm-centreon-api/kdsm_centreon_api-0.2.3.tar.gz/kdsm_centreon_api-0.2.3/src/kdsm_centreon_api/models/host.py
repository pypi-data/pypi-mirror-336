from datetime import datetime
from typing import Optional, List

from kdsm_centreon_api.models.base import Model
from kdsm_centreon_api.models.macro import Macro
from kdsm_centreon_api.models.min_obj import MonitoringServerMin, HostTemplateMin, TimeperiodMin, SeverityMin, HostGroupMin, ServiceRtmMin
from kdsm_centreon_api.models.snmp_version import SnmpVersion
from pydantic import Field, ConfigDict


class HostConfigurationList(Model):
    model_config = ConfigDict(use_enum_values=True)

    id: int = Field(default=..., description="The unique identifier of the host configuration.")
    name: str = Field(default=..., description="The name of the host configuration.")
    alias: Optional[str] = Field(default=None, description="The alias of the host configuration.")
    address: str = Field(default=..., description="The address of the host configuration.")
    monitoring_server: MonitoringServerMin = Field(default=..., description="The monitoring server of the host configuration.")
    templates: List[HostTemplateMin] = Field(default=..., description="The templates of the host configuration.")
    normal_check_interval: Optional[int] = Field(default=None, description="The normal check interval of the host configuration.")
    retry_check_interval: Optional[int] = Field(default=None, description="The retry check interval of the host configuration.")
    notification_timeperiod: Optional[TimeperiodMin] = Field(default=None, description="The notification timeperiod of the host configuration.")
    check_timeperiod: Optional[TimeperiodMin] = Field(default=None, description="The check timeperiod of the host configuration.")
    severity: Optional[SeverityMin] = Field(default=None, description="The severity of the host configuration.")
    # categories - ToDo - not implemented
    groups: List[HostGroupMin] = Field(default=..., description="The groups of the host configuration.")
    is_activated: bool = Field(default=..., description="The activation status of the host configuration.")


class HostConfigurationCreate(Model):
    monitoring_server_id: int = Field(default=..., description="The unique identifier of the monitoring server.")
    name: str = Field(default=..., description="The name of the host configuration.")
    address: str = Field(default=..., description="The address of the host configuration.")
    alias: str = Field(default=...,
                       description="The alias of the host configuration.")  # is required because bug in Centreon API see: https://github.com/centreon/centreon/issues/3909
    snmp_community: Optional[str] = Field(default=None, description="The SNMP community of the host configuration.")
    snmp_version: Optional[SnmpVersion] = Field(default=None, description="The SNMP version of the host configuration.")
    geo_coords: Optional[str] = Field(default=None, description="The geographical coordinates of the host configuration.")
    timezone_id: Optional[int] = Field(default=None, description="The unique identifier of the timezone.")
    severity_id: Optional[int] = Field(default=None, description="The unique identifier of the severity.")
    check_command_id: Optional[int] = Field(default=None, description="The unique identifier of the check command.")
    check_command_args: List[str] = Field(default_factory=list, description="The arguments of the check command.")
    max_check_attempts: Optional[int] = Field(default=None, description="The maximum check attempts of the host configuration.")
    normal_check_interval: Optional[int] = Field(default=None, description="The normal check interval of the host configuration.")
    retry_check_interval: Optional[int] = Field(default=None, description="The retry check interval of the host configuration.")
    active_check_enabled: int = Field(default=2, ge=0, le=2, description="The activation status of the active checks.")
    passive_check_enabled: int = Field(default=2, ge=0, le=2, description="The activation status of the passive checks.")
    notification_enabled: int = Field(default=2, ge=0, le=2, description="The activation status of the notifications.")
    notification_options: Optional[int] = Field(default=None, ge=0, le=31, description="The notification options of the host configuration. "
                                                                                       "The value is the sum of all the values of the selected options. "
                                                                                       "0 - NONE, "
                                                                                       "1 - DOWN, "
                                                                                       "2 - UNREACHABLE, "
                                                                                       "4 - RECOVERY, "
                                                                                       "8 - FLAPPING, "
                                                                                       "16 - DOWNTIME_SCHEDULED. "
                                                                                       "None - (inheritance of its parent's value. "
                                                                                       "If there is no parent, "
                                                                                       "the values used will be: DOWN, UNREACHABLE, RECOVERY, FLAPPING and DOWNTIME_SCHEDULED)."
                                                                                       "For example, a value equal to 5 corresponds to the selected options DOWN and RECOVERY.")
    notification_interval: Optional[int] = Field(default=None, description="The notification interval of the host configuration.")
    notification_timeperiod_id: Optional[int] = Field(default=None, description="The unique identifier of the notification timeperiod.")
    add_inherited_contact_group: bool = Field(default=False, description="The inheritance status of the contact group.")
    add_inherited_contact: bool = Field(default=False, description="The inheritance status of the contact.")
    first_notification_delay: Optional[int] = Field(default=None, description="The first notification delay of the host configuration.")
    recovery_notification_delay: Optional[int] = Field(default=None, description="The recovery notification delay of the host configuration.")
    acknowledgement_timeout: Optional[int] = Field(default=None, description="The acknowledgement timeout of the host configuration.")
    freshness_checked: int = Field(default=2, ge=0, le=2, description="The freshness check status of the host configuration.")
    freshness_threshold: Optional[int] = Field(default=None, description="The freshness threshold of the host configuration.")
    flap_detection_enabled: int = Field(default=2, ge=0, le=2, description="The flap detection status of the host configuration.")
    low_flap_threshold: Optional[int] = Field(default=None, description="The low flap threshold of the host configuration.")
    high_flap_threshold: Optional[int] = Field(default=None, description="The high flap threshold of the host configuration.")
    event_handler_enabled: int = Field(default=2, ge=0, le=2, description="The event handler status of the host configuration.")
    event_handler_command_id: Optional[int] = Field(default=None, description="The unique identifier of the event handler command.")
    event_handler_command_args: List[str] = Field(default_factory=list, description="The arguments of the event handler command.")
    note_url: Optional[str] = Field(default=None, max_length=65535, description="The note URL of the host configuration.")
    note: Optional[str] = Field(default=None, max_length=65535, description="The note of the host configuration.")
    action_url: Optional[str] = Field(default=None, max_length=65535, description="The action URL of the host configuration.")
    icon_id: Optional[int] = Field(default=None, description="The unique identifier of the icon.")
    icon_alternative: Optional[str] = Field(default=None, max_length=200, description="The alternative description of the icon.")
    comment: Optional[str] = Field(default=None, description="The comment of the host configuration.")
    is_activated: bool = Field(default=True, description="The activation status of the host configuration.")
    # categories - ToDo - not implemented
    groups: List[int] = Field(default_factory=list, description="The unique identifiers of the host groups.")
    templates: List[int] = Field(default_factory=list, description="The unique identifiers of the host templates.")
    macros: List[Macro] = Field(default_factory=list, description="The macros of the host configuration.")


class HostConfigurationCreated(HostConfigurationCreate):
    id: int = Field(default=..., description="The unique identifier of the host configuration.")
    groups: List[HostGroupMin] = Field(default_factory=list, description="The groups of the host configuration.")
    templates: List[HostTemplateMin] = Field(default_factory=list, description="The templates of the host configuration.")


class HostRtm(Model):
    id: int = Field(default=..., description="The unique identifier of the host configuration.")
    alias: str = Field(default=..., description="The alias of the host configuration.")
    display_name: str = Field(default=..., description="The display name of the host configuration.")
    name: str = Field(default=..., description="The name of the host configuration.")
    state: int = Field(default=..., ge=0, le=4, description="The state of the host configuration.")
    services: List[ServiceRtmMin] = Field(default_factory=list, description="The services of the host configuration.")
    poller_id: int = Field(default=..., description="The poller ID of the host configuration.")
    acknowledged: bool = Field(default=..., description="The acknowledgement status of the host configuration.")
    address_ip: str = Field(default=..., description="The IP address of the host configuration.")
    check_attempt: int = Field(default=..., description="The check attempt of the host configuration.")
    checked: bool = Field(default=..., description="The check status of the host configuration.")
    execution_time: float = Field(default=..., description="The execution time of the host configuration.")
    icon_image: str = Field(default=..., description="The icon image of the host configuration.")
    icon_image_alt: str = Field(default=..., description="The icon image alternative of the host configuration.")
    last_check: Optional[datetime] = Field(default=None, description="The last check of the host configuration.")
    last_hard_state_change: Optional[datetime] = Field(default=None, description="The last hard state change of the host configuration.")
    last_state_change: Optional[datetime] = Field(default=None, description="The last state change of the host configuration.")
    last_time_down: Optional[datetime] = Field(default=None, description="The last time down of the host configuration.")
    last_time_unreachable: Optional[datetime] = Field(default=None, description="The last time unreachable of the host configuration.")
    last_time_up: Optional[datetime] = Field(default=None, description="The last time up of the host configuration.")
    last_update: Optional[datetime] = Field(default=None, description="The last update of the host configuration.")
    max_check_attempts: int = Field(default=..., description="The maximum check attempts of the host configuration.")
    output: str = Field(default=..., description="The output of the host configuration.")
    passive_checks: bool = Field(default=..., description="The passive check status of the host configuration.")
    state_type: int = Field(default=..., ge=0, le=1, description="The state type of the host configuration.")
    timezone: str = Field(default=..., description="The timezone of the host configuration.")
    scheduled_downtime_depth: int = Field(default=..., description="The scheduled downtime depth of the host configuration.")
    criticality: Optional[int] = Field(default=None, description="The criticality of the host configuration.")
