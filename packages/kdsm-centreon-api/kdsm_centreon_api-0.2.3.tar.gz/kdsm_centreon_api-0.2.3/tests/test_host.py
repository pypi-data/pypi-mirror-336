from tests.conftest import skip_versions, CentreonVersion

from kdsm_centreon_api.api.utils import Sort, And
from kdsm_centreon_api.models.host import HostConfigurationCreate
from kdsm_centreon_api.models.macro import Macro


@skip_versions(CentreonVersion.v23_04, CentreonVersion.v22_10)
def test_host_list(centreon, test_host_name_rt_name):
    # find created host
    existing_host = centreon.host.find_host_configurations(name=test_host_name_rt_name, sort={"name": Sort.ASC})
    if len(existing_host) > 1:
        raise ValueError(f"Multiple hosts with the name '{test_host_name_rt_name}' found.")
    elif len(existing_host) == 0:
        raise ValueError(f"No host with the name '{test_host_name_rt_name}' found.")


@skip_versions(CentreonVersion.v23_04, CentreonVersion.v22_10)
def test_host_create(centreon,
                     test_monitoring_server_id,
                     test_command_id,
                     test_host_name,
                     test_host_group_rt_id,
                     test_host_template_id,
                     test_severity_id,
                     test_icon_id):
    # find existing host
    exiting_hosts = centreon.host.find_host_configurations(name=test_host_name)
    if len(exiting_hosts) > 1:
        raise ValueError(f"Multiple hosts with the name '{test_host_name}' found.")
    elif len(exiting_hosts) == 1:
        centreon.host.delete_host_configuration(exiting_hosts[0].id)

    # create new host
    new_host = HostConfigurationCreate(monitoring_server_id=test_monitoring_server_id,
                                       name=test_host_name,
                                       address="1.2.3.4",
                                       alias="test_host",
                                       snmp_community="public",
                                       snmp_version="1",
                                       geo_coords="0.0,0.0",
                                       timezone_id=1,
                                       severity_id=test_severity_id,
                                       check_command_id=test_command_id,
                                       check_command_args=["-H", "$HOSTADDRESS$", "-w", "3000,80%", "-c", "5000,90%"],
                                       max_check_attempts=3,
                                       normal_check_interval=5,
                                       retry_check_interval=1,
                                       active_check_enabled=2,
                                       passive_check_enabled=2,
                                       notification_enabled=2,
                                       notification_options=5,
                                       notification_interval=5,
                                       notification_timeperiod_id=1,
                                       add_inherited_contact_group=False,
                                       add_inherited_contact=False,
                                       first_notification_delay=0,
                                       recovery_notification_delay=0,
                                       acknowledgement_timeout=0,
                                       freshness_checked=2,
                                       freshness_threshold=0,
                                       flap_detection_enabled=2,
                                       low_flap_threshold=0,
                                       high_flap_threshold=0,
                                       event_handler_enabled=2,
                                       event_handler_command_id=test_command_id,
                                       event_handler_command_args=["-H", "$HOSTADDRESS$", "-w", "3000,80%", "-c", "5000,90%"],
                                       note_url="https://example.com",
                                       note="Test host",
                                       action_url="https://example.com",
                                       icon_id=1,
                                       icon_alternative="Test icon",
                                       comment="Test comment",
                                       is_activated=True,
                                       groups=[test_host_group_rt_id],
                                       templates=[test_host_template_id],
                                       macros=[
                                           Macro(name="TEST_MACRO",
                                                 value="test_value")
                                       ])
    host_created = centreon.host.create_host_configuration(new_host)

    # compare new host with created host
    for field_name, field in new_host.model_fields.items():
        field_value = getattr(new_host, field_name)
        field_value_created = getattr(host_created, field_name)

        if field_value != field_value_created:
            if field_name in ["groups", "templates"]:
                field_value_created = [sub_field.id for sub_field in field_value_created]
        if field_value != field_value_created:
            raise ValueError(f"Field '{field_name}' is different: {field_value} != {field_value_created}")

    # delete host configuration
    centreon.host.delete_host_configuration(host_created.id)


@skip_versions(CentreonVersion.v23_10, CentreonVersion.v23_04, CentreonVersion.v22_10)
def test_host_update(centreon,
                     test_monitoring_server_id,
                     test_command_id,
                     test_host_name,
                     test_host_group_rt_id,
                     test_host_template_id,
                     test_severity_id,
                     test_icon_id):
    # find existing host
    exiting_hosts = centreon.host.find_host_configurations(name=test_host_name, sort={"name": Sort.ASC})
    if len(exiting_hosts) > 1:
        raise ValueError(f"Multiple hosts with the name '{test_host_name}' found.")
    elif len(exiting_hosts) == 1:
        centreon.host.delete_host_configuration(exiting_hosts[0].id)

    # create new host
    new_host = HostConfigurationCreate(monitoring_server_id=test_monitoring_server_id,
                                       name=test_host_name,
                                       address="1.2.3.4",
                                       alias="test_host")
    host_created = centreon.host.create_host_configuration(new_host)

    # update host
    update_host = HostConfigurationCreate(monitoring_server_id=test_monitoring_server_id,
                                          name=test_host_name,
                                          address="5.6.7.8",
                                          alias="test_host_updated",
                                          snmp_community="public_updated",
                                          snmp_version="2c",
                                          geo_coords="1.0,1.0",
                                          timezone_id=2,
                                          severity_id=test_severity_id,
                                          check_command_id=test_command_id,
                                          check_command_args=["-H", "$HOSTADDRESS$", "-w", "6000,85%", "-c", "10000,95%"],
                                          max_check_attempts=6,
                                          normal_check_interval=10,
                                          retry_check_interval=2,
                                          active_check_enabled=0,
                                          passive_check_enabled=0,
                                          notification_enabled=0,
                                          notification_options=10,
                                          notification_interval=10,
                                          notification_timeperiod_id=2,
                                          add_inherited_contact_group=True,
                                          add_inherited_contact=True,
                                          first_notification_delay=1,
                                          recovery_notification_delay=1,
                                          acknowledgement_timeout=1,
                                          freshness_checked=0,
                                          freshness_threshold=1,
                                          flap_detection_enabled=0,
                                          low_flap_threshold=1,
                                          high_flap_threshold=1,
                                          event_handler_enabled=0,
                                          event_handler_command_id=test_command_id,
                                          event_handler_command_args=["-H", "$HOSTADDRESS$", "-w", "6000,85%", "-c", "10000,95%"],
                                          note_url="https://example.com/updated",
                                          note="Test host Updated",
                                          action_url="https://example.com/updated",
                                          icon_id=1,
                                          icon_alternative="Test icon updated",
                                          comment="Test comment updated",
                                          is_activated=False,
                                          groups=[test_host_group_rt_id],
                                          templates=[test_host_template_id],
                                          macros=[
                                              Macro(name="TEST_MACRO_UPDATED",
                                                    value="test_value_updated")
                                          ])
    centreon.host.update_host_configuration(host_created.id, update_host)

    # delete host configuration
    centreon.host.delete_host_configuration(host_created.id)


@skip_versions(CentreonVersion.v23_04, CentreonVersion.v22_10)
def test_host_apply(centreon,
                    test_monitoring_server_id,
                    test_host_name):
    # find existing host
    exiting_hosts = centreon.host.find_host_configurations(name=test_host_name, sort={"name": Sort.ASC})
    if len(exiting_hosts) > 1:
        raise ValueError(f"Multiple hosts with the name '{test_host_name}' found.")
    elif len(exiting_hosts) == 1:
        centreon.host.delete_host_configuration(exiting_hosts[0].id)

    # create new host
    new_host = HostConfigurationCreate(monitoring_server_id=test_monitoring_server_id,
                                       name=test_host_name,
                                       address="1.2.3.4",
                                       alias="test_host")
    host_created = centreon.host.create_host_configuration(new_host)

    # apply host configuration
    centreon.host.apply_host_configuration(host_created.name)

    # delete host configuration
    centreon.host.delete_host_configuration(host_created.id)


def test_host_list_rtm(centreon,
                       test_host_name_rt_name):
    # find existing rtm host
    existing_rtm_host_rtm = centreon.host.list_hosts(And(host_name=test_host_name_rt_name),
                                                     sort={"host_name": Sort.ASC})
    if len(existing_rtm_host_rtm) > 1:
        raise ValueError(f"Multiple hosts with the name '{existing_rtm_host_rtm}' found.")
    elif len(existing_rtm_host_rtm) == 0:
        raise ValueError(f"No host with the name '{existing_rtm_host_rtm}' found.")
