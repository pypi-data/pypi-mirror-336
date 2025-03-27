from typing import Optional, List

from kdsm_centreon_api.models.base import Model
from kdsm_centreon_api.models.macro import Macro
from pydantic.fields import Field


class ServiceTemplateList(Model):
    id: int = Field(default=..., description="The unique identifier of the service template.")
    is_locked: bool = Field(default=..., description="Indicates whether the configuration is locked for editing or not")
    name: str = Field(default=..., description="The name of the service template.")
    alias: str = Field(default=..., description="The alias of the service template.")
    comment: Optional[str] = Field(default=None, description="service template comments")
    service_template_id: Optional[int] = Field(default=None, ge=1, description="Service template ID")
    check_command_id: Optional[int] = Field(default=None, description="Check command ID")
    check_command_args: List[str] = Field(default_factory=list, description="Check command arguments")
    check_timeperiod_id: Optional[int] = Field(default=None, description="Check command timeperiod ID")
    max_check_attempts: Optional[int] = Field(default=None,
                                              description="Define the number of times that the monitoring engine will retry the service check command "
                                                          "if it returns any non-OK state")
    normal_check_interval: Optional[int] = Field(default=None, description="Define the number of 'time units' between regularly scheduled checks of the service.")
    retry_check_interval: Optional[int] = Field(default=None,
                                                description="Define the number of 'time units' to wait before scheduling "
                                                            "a re-check for this service after a non-UP state was detected.")
    active_check_enabled: int = Field(default=2, ge=0, le=2, description="Indicates whether active checks are enabled or not")
    passive_check_enabled: int = Field(default=2, ge=0, le=2, description="Indicates whether passive checks are enabled or not")
    volatility_enabled: int = Field(default=2, ge=0, le=2, description="Indicates whether the service is 'volatile' or not")
    notification_enabled: int = Field(default=2, ge=0, le=2, description="Specify whether notifications for this service are enabled or not")
    is_contact_additive_inheritance: bool = Field(default=False, description="Only used when notification inheritance for hosts and services is set to vertical inheritance only.")
    is_contact_group_additive_inheritance: bool = Field(default=False,
                                                        description="Only used when notification inheritance for hosts and services is set to vertical inheritance only.")
    notification_interval: Optional[int] = Field(default=None,
                                                 description="Define the number of 'time units' to wait before re-notifying a contact that "
                                                             "this service is still down or unreachable.")
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
    notification_timeperiod_id: Optional[int] = Field(default=None, description="Notification timeperiod ID")
    first_notification_delay: Optional[int] = Field(default=None,
                                                    description="Define the number of 'time units' to wait before sending out the first problem "
                                                                "notification when this service enters a non-UP state.")
    recovery_notification_delay: Optional[int] = Field(default=None,
                                                       description="Define the number of 'time units' to wait before sending out the recovery "
                                                                   "notification when this service enters an UP state.")
    acknowledgement_timeout: Optional[int] = Field(default=None, description="Specify a duration of acknowledgement for this service.")
    freshness_checked: int = Field(default=2, ge=0, le=2, description="Indicates whether freshness is checked or not")
    freshness_threshold: Optional[int] = Field(default=None, description="Specify the freshness threshold (in seconds) for this service.")
    flap_detection_enabled: int = Field(default=2, ge=0, le=2, description="Indicates whether the flap detection is enabled or not")
    low_flap_threshold: Optional[int] = Field(default=None, description="Specify the low state change threshold used in flap detection for this service")
    high_flap_threshold: Optional[int] = Field(default=None, description="Specify the high state change threshold used in flap detection for this service")
    event_handler_enabled: int = Field(default=2, ge=0, le=2, description="Indicates whether the event handler is enabled or not")
    event_handler_command_id: Optional[int] = Field(default=None, description="Event handler command ID")
    event_handler_command_args: List[str] = Field(default_factory=list, description="Event handler command arguments")
    graph_template_id: Optional[int] = Field(default=None, ge=1, description="ID of the default graph template that will be used for this service.")
    note: Optional[str] = Field(default=None, max_length=65535, description="Define an optional note.")
    note_url: Optional[str] = Field(default=None, max_length=65535, description="Define an optional URL that can be used to provide more information about the service.")
    action_url: Optional[str] = Field(default=None, max_length=65535, description="Define an optional URL that can be used to provide more actions to be performed on the service.")
    icon_id: Optional[int] = Field(default=None, description="Define the image ID that should be associated with this service template")
    icon_alternative: Optional[str] = Field(default=None, max_length=200, description="Define an optional string that is used in the alternative description of the icon image")
    severity_id: Optional[int] = Field(default=None, description="Severity ID")
    host_templates: List[int] = Field(default_factory=list, description="Array of host templates")
    # service_categories - ToDo - not implemented
    # service_groups - ToDo - not implemented
    macros: List[Macro] = Field(default_factory=list, description="Array of objects (macro)")
