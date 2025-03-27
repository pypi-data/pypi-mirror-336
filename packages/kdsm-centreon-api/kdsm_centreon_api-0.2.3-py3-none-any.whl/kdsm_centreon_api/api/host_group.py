from typing import Optional, Dict, List

from kdsm_centreon_api.api.centreon_version import CentreonVersion
from kdsm_centreon_api.api.sub_api import SubApi
from kdsm_centreon_api.api.utils import validate, SearchType, Sort, sort_dump, exclude_on_versions
from kdsm_centreon_api.logger import logger
from kdsm_centreon_api.models.host_group import HostGroupConfigurationList, HostGroupConfigurationCreate, HostGroupConfigurationCreated


class HostGroup(SubApi):
    @validate({"id": "id",
               "name": "name",
               "alias": "alias",
               "is_activated": "is_activated",
               "hostcategory_id": "hostcategory.id",
               "hostcategory_name": "hostcategory.name"})
    def find_host_group_configurations(self,
                                       search: Optional[SearchType] = None,
                                       limit: int = 1000,
                                       page: int = 1,
                                       sort: Optional[Dict[str, Sort]] = None) -> List[HostGroupConfigurationList]:
        logger.debug(f"List host groups from {self}.")

        # params
        params = {
            "search": search.dump(),
            "limit": limit,
            "page": page
        }

        if sort is not None:
            # dump sort
            params["sort_by"] = sort_dump(sort)

        result = self.request_v2(method="GET",
                                 api_path="/configuration/hosts/groups",
                                 error_message=f"Could not list host groups from {self}.",
                                 params=params)
        host_groups_dicts = result["result"]

        # parse to HostGroupConfigurationList
        host_groups = []
        for host_group_dict in host_groups_dicts:
            host_group = HostGroupConfigurationList.model_validate(host_group_dict)
            host_groups.append(host_group)

        logger.debug(f"List host groups from {self} successful. -> {len(host_groups)} host groups")

        return host_groups

    @exclude_on_versions(CentreonVersion.v23_04, CentreonVersion.v22_10)
    def get_host_group_configuration(self, host_group_id: int) -> HostGroupConfigurationCreated:
        logger.debug(f"Get host group '{host_group_id}' from {self}.")

        host_group_dict = self.request_v2(method="GET",
                                          api_path=f"/configuration/hosts/groups/{host_group_id}",
                                          error_message=f"Could not get host group '{host_group_id}' from {self}.")

        # parse to HostGroupConfigurationCreated
        host_group = HostGroupConfigurationCreated.model_validate(host_group_dict)

        logger.debug(f"Get host group '{host_group_id}' from {self} successful.")

        return host_group

    @exclude_on_versions(CentreonVersion.v22_10)
    def create_host_group_configuration(self, host_group: HostGroupConfigurationCreate) -> HostGroupConfigurationCreated:
        logger.debug(f"Create host group '{host_group.name}' on {self}.")

        host_group_dict = host_group.model_dump(exclude_none=True)

        host_group_created_dict = self.request_v2(method="POST",
                                                  api_path="/configuration/hosts/groups",
                                                  error_message=f"Could not create host group '{host_group.name}' on {self}.",
                                                  data=host_group_dict)

        # parse to HostGroupConfigurationCreated
        host_group_created = HostGroupConfigurationCreated.model_validate(host_group_created_dict)

        logger.debug(f"Create host group '{host_group_created.name}' on {self} successful.")

        return host_group_created

    @exclude_on_versions(CentreonVersion.v23_04, CentreonVersion.v22_10)
    def update_host_group_configuration(self, host_group_id: int, host: HostGroupConfigurationCreate) -> None:
        logger.debug(f"Update host group '{host_group_id}' on {self}.")

        host_dict = host.model_dump(exclude_none=True)

        self.request_v2(method="PUT",
                        api_path=f"/configuration/hosts/groups/{host_group_id}",
                        error_message=f"Could not update host group '{host_group_id}' on {self}.",
                        data=host_dict)

        logger.debug(f"Update host group '{host_group_id}' on {self} successful.")

        return None

    @exclude_on_versions(CentreonVersion.v22_10)
    def delete_host_group_configuration(self, host_group_id: int) -> None:
        logger.debug(f"Delete host group '{host_group_id}' from {self}.")

        self.request_v2(method="DELETE", api_path=f"/configuration/hosts/groups/{host_group_id}", error_message=f"Could not delete host group '{host_group_id}' from {self}.")

        logger.debug(f"Delete host group '{host_group_id}' from {self} successful.")
