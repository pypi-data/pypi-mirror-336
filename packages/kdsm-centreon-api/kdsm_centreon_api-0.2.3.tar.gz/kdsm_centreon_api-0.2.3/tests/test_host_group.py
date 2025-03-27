from tests.conftest import skip_versions
from kdsm_centreon_api.api.centreon_version import CentreonVersion
from kdsm_centreon_api.api.utils import Sort
from kdsm_centreon_api.models.host_group import HostGroupConfigurationCreate


def test_host_group_list(centreon, test_host_group_rt_name):
    # find existing host group
    exiting_host_groups = centreon.host_group.find_host_group_configurations(name=test_host_group_rt_name, sort={"name": Sort.ASC})
    if len(exiting_host_groups) > 1:
        raise ValueError(f"Multiple host groups with the name '{test_host_group_rt_name}' found.")
    elif len(exiting_host_groups) == 0:
        raise ValueError(f"No host group with the name '{test_host_group_rt_name}' found.")


@skip_versions(CentreonVersion.v23_04, CentreonVersion.v22_10)
def test_host_group_get(centreon, test_host_group_rt_id):
    # get existing host group
    exiting_host_groups = centreon.host_group.get_host_group_configuration(test_host_group_rt_id)
    if exiting_host_groups.id != test_host_group_rt_id:
        raise ValueError(f"Host group ID '{test_host_group_rt_id}' not found.")


@skip_versions(CentreonVersion.v22_10)
def test_host_group_create(centreon, test_host_group_name, test_icon_id):
    # find existing host group
    exiting_host_groups = centreon.host_group.find_host_group_configurations(name=test_host_group_name)
    if len(exiting_host_groups) > 1:
        raise ValueError(f"Multiple host groups with the name '{test_host_group_name}' found.")
    elif len(exiting_host_groups) == 1:
        centreon.host_group.delete_host_group_configuration(exiting_host_groups[0].id)

    # create new host group
    new_host_group = HostGroupConfigurationCreate(name=test_host_group_name,
                                                  alias="Test Host Group",
                                                  notes="Test Host Group Notes",
                                                  notes_url="https://www.example.com",
                                                  action_url="https://www.example.com/action",
                                                  icon_id=test_icon_id,
                                                  icon_map_id=test_icon_id,
                                                  geo_coords="0.0,0.0",
                                                  rrd=1,
                                                  comment="Test Host Group Comment",
                                                  is_activated=True)
    host_group_created = centreon.host_group.create_host_group_configuration(new_host_group)

    # compare new host group with created host group
    for field_name, field in new_host_group.model_fields.items():
        field_value = getattr(new_host_group, field_name)
        field_value_created = getattr(host_group_created, field_name)

        if field_value != field_value_created:
            raise ValueError(f"Field '{field_name}' is different: {field_value} != {field_value_created}")

    # delete host group configuration
    centreon.host_group.delete_host_group_configuration(host_group_created.id)


@skip_versions(CentreonVersion.v23_04, CentreonVersion.v22_10)
def test_host_group_update(centreon, test_host_group_name, test_icon_id):
    # find existing host group
    exiting_host_groups = centreon.host_group.find_host_group_configurations(name=test_host_group_name)
    if len(exiting_host_groups) > 1:
        raise ValueError(f"Multiple host groups with the name '{test_host_group_name}' found.")
    elif len(exiting_host_groups) == 1:
        centreon.host_group.delete_host_group_configuration(exiting_host_groups[0].id)

    # create new host group
    new_host_group = HostGroupConfigurationCreate(name=test_host_group_name)
    host_group_created = centreon.host_group.create_host_group_configuration(new_host_group)

    # update new host group
    update_host_group = HostGroupConfigurationCreate(name=test_host_group_name,
                                                     alias="Test Host Group",
                                                     notes="Test Host Group Notes",
                                                     notes_url="https://www.example.com",
                                                     action_url="https://www.example.com/action",
                                                     icon_id=test_icon_id,
                                                     icon_map_id=test_icon_id,
                                                     geo_coords="0.0,0.0",
                                                     rrd=1,
                                                     comment="Test Host Group Comment",
                                                     is_activated=True)
    centreon.host_group.update_host_group_configuration(host_group_created.id, update_host_group)

    # delete host group configuration
    centreon.host_group.delete_host_group_configuration(host_group_created.id)
