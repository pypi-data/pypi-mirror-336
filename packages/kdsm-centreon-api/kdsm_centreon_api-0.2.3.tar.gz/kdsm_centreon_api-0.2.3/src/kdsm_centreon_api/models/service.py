from datetime import datetime
from typing import Optional, List

from kdsm_centreon_api.models.base import Model
from kdsm_centreon_api.models.macro import Macro
from kdsm_centreon_api.models.min_obj import TimeperiodMin, SeverityMin, HostMin, ServiceTemplateMin, ServiceGroupMin
from kdsm_centreon_api.models.resource_status import ResourceStatus
from pydantic import Field


class ServiceConfigurationList(Model):
    id: int = Field(default=..., description="The unique identifier of the service configuration.")
    name: str = Field(default=..., description="The name of the service configuration.")
    hosts: List[HostMin] = Field(default=..., description="The hosts of the service configuration.")
    service_template: Optional[ServiceTemplateMin] = Field(default=None, description="The service template of the service configuration.")
    check_timeperiod: Optional[TimeperiodMin] = Field(default=None, description="The check timeperiod of the service configuration.")
    severity: Optional[SeverityMin] = Field(default=None, description="The severity of the service configuration.")
    notification_timeperiod: Optional[TimeperiodMin] = Field(default=None, description="The notification timeperiod of the service configuration.")
    # categories - ToDo - not implemented
    groups: List[ServiceGroupMin] = Field(default=..., description="The groups of the service configuration.")
    normal_check_interval: Optional[int] = Field(default=None, description="The normal check interval of the service configuration.")
    retry_check_interval: Optional[int] = Field(default=None, description="The retry check interval of the service configuration.")
    is_activated: bool = Field(default=..., description="The activation status of the service configuration.")


class ServiceConfigurationCreate(Model):
    name: str = Field(default=..., description="Service name.")
    host_id: int = Field(default=..., description="ID of the host linked to this service.")
    geo_coords: Optional[str] = Field(default=None, description="Geographic coordinates of the service")
    comment: Optional[str] = Field(default=None, description="Service comment.")
    service_template_id: Optional[int] = Field(default=None, ge=1, description="Template ID of the service template.")
    check_command_id: Optional[int] = Field(default=None, ge=1, description="Check command ID.")
    check_command_args: List[str] = Field(default_factory=list, description="Array of strings")
    check_timeperiod_id: Optional[int] = Field(default=None, ge=1, description="Time period ID of the check command.")
    max_check_attempts: Optional[int] = Field(default=None, description="The maximum check attempts of the service.")
    normal_check_interval: Optional[int] = Field(default=None, description="The normal check interval of the service.")
    retry_check_interval: Optional[int] = Field(default=None, description="The retry check interval of the service.")
    active_check_enabled: int = Field(default=2, ge=0, le=2, description="Indicates whether active checks are enabled or not.")
    passive_check_enabled: int = Field(default=2, ge=0, le=2, description="Indicates whether passive checks are enabled or not.")
    volatility_enabled: int = Field(default=2, ge=0, le=2, description="Indicates whether the service is 'volatile' or not.")
    notification_enabled: int = Field(default=2, ge=0, le=2, description="Specify whether notifications are enabled or not.")
    is_contact_additive_inheritance: bool = Field(default=False, description="Only used when notification inheritance for hosts and services is set to vertical inheritance only.")
    is_contact_group_additive_inheritance: bool = Field(default=False,
                                                        description="Only used when notification inheritance for hosts and services is set to vertical inheritance only.")
    notification_interval: Optional[int] = Field(default=None, description="The notification interval of the service.")
    notification_timeperiod_id: Optional[int] = Field(default=None, description="Notification timeperiod ID.")
    notification_type: Optional[int] = Field(default=None, ge=0, le=63, description="The notification options of the service configuration. "
                                                                                    "The value is the sum of all the values of the selected options. "
                                                                                    "0 - NONE, "
                                                                                    "1 - WARNING, "
                                                                                    "2 - UNKNOWN, "
                                                                                    "4 - CRITICAL, "
                                                                                    "8 - RECOVERY, "
                                                                                    "16 - FLAPPING, "
                                                                                    "32 - DOWNTIME_SCHEDULED. "
                                                                                    "None - (inheritance of its parent's value. "
                                                                                    "If there is no parent, "
                                                                                    "the values used will be: WARNING, UNKNOWN, CRITICAL, "
                                                                                    "RECOVERY, FLAPPING and DOWNTIME_SCHEDULED)."
                                                                                    "For example, a value equal to 5 corresponds to the selected options WARNING and RECOVERY.")
    first_notification_delay: Optional[int] = Field(default=None, description="The first notification delay of the service.")
    recovery_notification_delay: Optional[int] = Field(default=None, description="The recovery notification delay of the service.")
    acknowledgement_timeout: Optional[int] = Field(default=None, description="The acknowledgement timeout of the service.")
    freshness_checked: int = Field(default=2, ge=0, le=2, description="Indicates whether freshness is checked or not.")
    freshness_threshold: Optional[int] = Field(default=None, description="The freshness threshold of the service.")
    flap_detection_enabled: int = Field(default=2, ge=0, le=2, description="Indicates whether the flap detection is enabled or not.")
    low_flap_threshold: Optional[int] = Field(default=None, description="The low flap threshold of the service.")
    high_flap_threshold: Optional[int] = Field(default=None, description="The high flap threshold of the service.")
    event_handler_enabled: int = Field(default=2, ge=0, le=2, description="Indicates whether the event handler is enabled or not.")
    event_handler_command_id: Optional[int] = Field(default=None, ge=1, description="Event handler command ID.")
    event_handler_command_args: List[str] = Field(default_factory=list, description="Array of strings")
    graph_template_id: Optional[int] = Field(default=None, ge=1, description="ID of the default graph template that will be used for this service.")
    note: Optional[str] = Field(default=None, description="Define an optional note.")
    note_url: Optional[str] = Field(default=None, description="Define an optional URL that can be used to provide more information about the service.")
    action_url: Optional[str] = Field(default=None, description="Define an optional URL that can be used to specify actions to be performed on the service.")
    icon_id: Optional[int] = Field(default=None, ge=1, description="Define the image ID that should be associated with this service.")
    icon_alternative: Optional[str] = Field(default=None, description="Define an optional string that is used as an alternative description for the icon.")
    severity_id: Optional[int] = Field(default=None, ge=1, description="Severity ID.")
    is_activated: bool = Field(default=True, description="Indicates whether the service is activated or not.")
    # service_categories - ToDo - not implemented
    service_groups: List[int] = Field(default_factory=list, description="Array of integers")
    macros: List[Macro] = Field(default_factory=list, description="Array of objects (macro)")


class ServiceConfigurationCreated(ServiceConfigurationCreate):
    id: int = Field(default=..., description="The unique identifier of the service configuration.")
    service_groups: List[ServiceGroupMin] = Field(default=..., alias="groups", description="The groups of the service configuration.")


class ServiceRtm(Model):
    id: int = Field(default=..., description="The unique identifier of the service.")
    description: str = Field(default=..., description="The description of the service.")
    state: int = Field(default=..., ge=0, le=4, description="The state of the service.")
    check_attempt: int = Field(default=..., description="The check attempt of the service.")
    icon_image: str = Field(default=..., description="The icon image of the service.")
    icon_image_alt: str = Field(default=..., description="The icon image alternative of the service.")
    last_check: Optional[datetime] = Field(default=None, description="The last check of the service.")
    last_state_change: Optional[datetime] = Field(default=None, description="The last state change of the service.")
    max_check_attempts: int = Field(default=..., description="The maximum check attempts of the service.")
    output: str = Field(default=..., description="The output of the service.")
    state_type: int = Field(default=..., ge=0, le=1, description="The state type of the service.")
    criticality: Optional[int] = Field(default=None, description="The criticality of the service.")
    status: ResourceStatus = Field(default=..., description="The status of the service.")
    duration: Optional[str] = Field(default=None, description="The duration of the service.")
