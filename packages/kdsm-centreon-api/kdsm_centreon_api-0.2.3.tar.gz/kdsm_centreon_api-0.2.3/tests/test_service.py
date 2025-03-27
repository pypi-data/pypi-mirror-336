from tests.conftest import skip_versions, CentreonVersion

from kdsm_centreon_api.api.utils import Sort, And
from kdsm_centreon_api.models.host import HostConfigurationCreate
from kdsm_centreon_api.models.macro import Macro
from kdsm_centreon_api.models.service import ServiceConfigurationCreate


@skip_versions(CentreonVersion.v23_04, CentreonVersion.v22_10)
def test_service_list(centreon,
                      test_host_name_rt_name,
                      test_service_name_rt_name):
    # find existing rtm service
    existing_service_ = centreon.service.find_service_configurations(And(host_name=test_host_name_rt_name, name=test_service_name_rt_name),
                                                                     sort={"name": Sort.ASC})
    if len(existing_service_) > 1:
        raise ValueError(f"Multiple services with the name '{test_service_name_rt_name}' found.")
    elif len(existing_service_) == 0:
        raise ValueError(f"No service with the name '{test_service_name_rt_name}' found.")


@skip_versions(CentreonVersion.v23_04, CentreonVersion.v22_10)
def test_service_create(centreon,
                        test_monitoring_server_id,
                        test_icon_id,
                        test_host_name,
                        test_service_name,
                        test_command_id,
                        test_service_group_rt_id,
                        test_service_template_id):
    # find existing host
    exiting_hosts = centreon.host.find_host_configurations(name=test_host_name, sort={"name": Sort.ASC})
    if len(exiting_hosts) > 1:
        raise ValueError(f"Multiple hosts with the name '{test_host_name}' found.")
    elif len(exiting_hosts) == 1:
        centreon.host.delete_host_configuration(exiting_hosts[0].id)

    # create new host
    new_host = HostConfigurationCreate(monitoring_server_id=test_monitoring_server_id,
                                       name=test_host_name,
                                       alias="test_host",
                                       address="1.2.3.4")
    host_created = centreon.host.create_host_configuration(new_host)

    # create new service
    new_service = ServiceConfigurationCreate(name=test_service_name,
                                             host_id=host_created.id,
                                             geo_coords="0.0,0.0",
                                             comment="Test comment",
                                             service_template_id=test_service_template_id,
                                             check_command_id=test_command_id,
                                             check_command_args=["-H", "$HOSTADDRESS$", "-w", "3000,80%", "-c", "5000,90%"],
                                             check_timeperiod_id=1,
                                             max_check_attempts=3,
                                             normal_check_interval=5,
                                             retry_check_interval=1,
                                             active_check_enabled=2,
                                             passive_check_enabled=2,
                                             volatility_enabled=2,
                                             notification_enabled=2,
                                             is_contact_additive_inheritance=False,
                                             is_contact_group_additive_inheritance=False,
                                             notification_interval=5,
                                             notification_timeperiod_id=1,
                                             notification_type=1,
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
                                             graph_template_id=1,
                                             note="Test service",
                                             note_url="https://example.com",
                                             action_url="https://example.com",
                                             icon_id=test_icon_id,
                                             icon_alternative="Test icon",
                                             is_activated=True,
                                             service_groups=[test_service_group_rt_id],
                                             macros=[
                                                 Macro(name="TEST_MACRO",
                                                       value="test_value")
                                             ])
    service_created = centreon.service.create_service_configuration(new_service)

    # compare new service with created service
    for field_name, field in new_service.model_fields.items():
        field_value = getattr(new_service, field_name)
        field_value_created = getattr(service_created, field_name)

        if field_value != field_value_created:
            if field_name in ["service_groups"]:
                field_value_created = [sub_field.id for sub_field in field_value_created]
        if field_value != field_value_created:
            raise ValueError(f"Field '{field_name}' is different: {field_value} != {field_value_created}")

    # delete service configuration
    centreon.service.delete_service_configuration(service_created.id)

    # delete host configuration
    centreon.host.delete_host_configuration(host_created.id)


@skip_versions(CentreonVersion.v23_10, CentreonVersion.v23_04, CentreonVersion.v22_10)
def test_service_update(centreon,
                        test_monitoring_server_id,
                        test_icon_id,
                        test_host_name,
                        test_service_name,
                        test_command_id,
                        test_service_group_rt_id,
                        test_service_template_id):
    # find existing host
    exiting_hosts = centreon.host.find_host_configurations(name=test_host_name, sort={"name": Sort.ASC})
    if len(exiting_hosts) > 1:
        raise ValueError(f"Multiple hosts with the name '{test_host_name}' found.")
    elif len(exiting_hosts) == 1:
        centreon.host.delete_host_configuration(exiting_hosts[0].id)

    # create new host
    new_host = HostConfigurationCreate(monitoring_server_id=test_monitoring_server_id,
                                       name=test_host_name,
                                       alias="test_host",
                                       address="1.2.3.4")
    host_created = centreon.host.create_host_configuration(new_host)

    # create new service
    new_service = ServiceConfigurationCreate(name=test_service_name,
                                             host_id=host_created.id,
                                             service_template_id=test_service_template_id)
    service_created = centreon.service.create_service_configuration(new_service)

    # update service
    update_service = ServiceConfigurationCreate(name=test_service_name,
                                                host_id=host_created.id,
                                                geo_coords="0.0,0.0",
                                                comment="Test comment",
                                                service_template_id=test_service_template_id,
                                                check_command_id=test_command_id,
                                                check_command_args=["-H", "$HOSTADDRESS$", "-w", "3000,80%", "-c", "5000,90%"],
                                                check_timeperiod_id=1,
                                                max_check_attempts=3,
                                                normal_check_interval=5,
                                                retry_check_interval=1,
                                                active_check_enabled=2,
                                                passive_check_enabled=2,
                                                volatility_enabled=2,
                                                notification_enabled=2,
                                                is_contact_additive_inheritance=False,
                                                is_contact_group_additive_inheritance=False,
                                                notification_interval=5,
                                                notification_timeperiod_id=1,
                                                notification_type=1,
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
                                                graph_template_id=1,
                                                note="Test service",
                                                note_url="https://example.com",
                                                action_url="https://example.com",
                                                icon_id=test_icon_id,
                                                icon_alternative="Test icon",
                                                is_activated=True,
                                                service_groups=[test_service_group_rt_id],
                                                macros=[
                                                    Macro(name="TEST_MACRO",
                                                          value="test_value")
                                                ])
    centreon.service.update_service_configuration(service_created.id, update_service)

    # delete service configuration
    centreon.service.delete_service_configuration(service_created.id)

    # delete host configuration
    centreon.host.delete_host_configuration(host_created.id)


def test_service_rtm(centreon,
                     test_host_name_rt_id,
                     test_service_name_rt_name):
    # find existing rtm service
    existing_rtm_service_rtm = centreon.service.get_service_related_to_host(test_host_name_rt_id, And(service_description=test_service_name_rt_name),
                                                                            sort={"service_description": Sort.ASC})
    if len(existing_rtm_service_rtm) > 1:
        raise ValueError(f"Multiple services with the description '{test_service_name_rt_name}' found.")
    elif len(existing_rtm_service_rtm) == 0:
        raise ValueError(f"No service with the description '{test_service_name_rt_name}' found.")
