from typing import Optional, List

from kdsm_centreon_api.models.base import Model
from kdsm_centreon_api.models.snmp_version import SnmpVersion
from pydantic.fields import Field


class HostTemplateList(Model):
    id: int = Field(default=..., description="The unique identifier of the host template.")
    name: str = Field(default=..., description="The name of the host template.")
    alias: Optional[str] = Field(default=None, description="The alias of the host template.")
    snmp_community: Optional[str] = Field(default=None, description="Community of the SNMP agent")
    snmp_version: Optional[SnmpVersion] = Field(default=None, description="Version of the SNMP agent.")
    timezone_id: Optional[int] = Field(default=None, description="Timezone ID")
    severity_id: Optional[int] = Field(default=None, description="Severity ID")
    check_command_id: Optional[int] = Field(default=None, description="Check command ID")
    check_command_args: List[str] = Field(default_factory=list, description="Check command arguments")
    check_timeperiod_id: Optional[int] = Field(default=None, description="Check command timeperiod ID")
    max_check_attempts: Optional[int] = Field(default=None,
                                              description="Define the number of times that the monitoring engine will retry the host check command if it returns any non-OK state")
    normal_check_interval: Optional[int] = Field(default=None, description="Define the number of 'time units' between regularly scheduled checks of the host.")
    retry_check_interval: Optional[int] = Field(default=None,
                                                description="Define the number of 'time units' to wait before scheduling "
                                                            "a re-check for this host after a non-UP state was detected.")
    active_check_enabled: int = Field(default=2, ge=0, le=2, description="Indicates whether active checks are enabled or not")
    passive_check_enabled: int = Field(default=2, ge=0, le=2, description="Indicates whether passive checks are enabled or not")
    notification_enabled: int = Field(default=2, ge=0, le=2, description="Specify whether notifications for this host are enabled or not")
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
    notification_interval: Optional[int] = Field(default=None,
                                                 description="Define the number of 'time units' to wait before re-notifying a contact that this host is still down or unreachable.")
    notification_timeperiod_id: Optional[int] = Field(default=None, description="Notification timeperiod ID")
    add_inherited_contact_group: bool = Field(default=False, description="Only used when notification inheritance for hosts and services is set to vertical inheritance only.")
    add_inherited_contact: bool = Field(default=False, description="Only used when notification inheritance for hosts and services is set to vertical inheritance only.")
    first_notification_delay: Optional[int] = Field(default=None,
                                                    description="Define the number of 'time units' to wait before sending out the first problem notification "
                                                                "when this host enters a non-UP state.")
    recovery_notification_delay: Optional[int] = Field(default=None,
                                                       description="Define the number of 'time units' to wait before sending out the recovery notification "
                                                                   "when this host enters an UP state.")
    acknowledgement_timeout: Optional[int] = Field(default=None, description="Specify a duration of acknowledgement for this host.")
    freshness_checked: int = Field(default=2, ge=0, le=2, description="Indicates whether freshness is checked or not")
    freshness_threshold: Optional[int] = Field(default=None, description="Specify the freshness threshold (in seconds) for this host.")
    flap_detection_enabled: int = Field(default=2, ge=0, le=2, description="Indicates whether the flap detection is enabled or not")
    low_flap_threshold: Optional[int] = Field(default=None, description="Specify the low state change threshold used in flap detection for this host")
    high_flap_threshold: Optional[int] = Field(default=None, description="Specify the high state change threshold used in flap detection for this host")
    event_handler_enabled: int = Field(default=2, ge=0, le=2, description="Indicates whether the event handler is enabled or not")
    event_handler_command_id: Optional[int] = Field(default=None, description="Event handler command ID")
    event_handler_command_args: List[str] = Field(default_factory=list, description="Event handler command arguments")
    note_url: Optional[str] = Field(default=None, max_length=65535, description="Define an optional URL that can be used to provide more information about the host.")
    note: Optional[str] = Field(default=None, max_length=65535, description="Define an optional note.")
    action_url: Optional[str] = Field(default=None, max_length=65535, description="Define an optional URL that can be used to provide more actions to be performed on the host.")
    icon_id: Optional[int] = Field(default=None, description="Define the image ID that should be associated with this host template")
    icon_alternative: Optional[str] = Field(default=None, max_length=200, description="Define an optional string that is used in the alternative description of the icon image")
    comment: Optional[str] = Field(default=None, description="Host template comments")
    is_locked: bool = Field(default=..., description="Indicates whether the configuration is locked for editing or not")
