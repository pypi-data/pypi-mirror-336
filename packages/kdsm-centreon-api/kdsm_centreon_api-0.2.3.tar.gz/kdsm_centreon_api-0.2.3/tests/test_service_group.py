from kdsm_centreon_api.api.centreon_version import CentreonVersion
from kdsm_centreon_api.api.utils import Sort

from tests.conftest import skip_versions


@skip_versions(CentreonVersion.v22_10)
def test_service_group_list(centreon, test_service_group_rt_name):
    # find existing service group
    exiting_service_groups = centreon.service_group.find_service_group_configurations(name=test_service_group_rt_name, sort={"name": Sort.ASC})
    if len(exiting_service_groups) > 1:
        raise ValueError(f"Multiple service groups with the name '{test_service_group_rt_name}' found.")
    elif len(exiting_service_groups) == 0:
        raise ValueError(f"No service group with the name '{test_service_group_rt_name}' found.")
