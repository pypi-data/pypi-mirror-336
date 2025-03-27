from typing import Optional, Dict, List

from kdsm_centreon_api.api.centreon_version import CentreonVersion
from kdsm_centreon_api.api.sub_api import SubApi
from kdsm_centreon_api.api.utils import validate, SearchType, Sort, sort_dump, exclude_on_versions
from kdsm_centreon_api.logger import logger
from kdsm_centreon_api.models.service_group import ServiceGroupConfigurationList


class ServiceGroup(SubApi):
    @exclude_on_versions(CentreonVersion.v22_10)
    @validate({"id": "id",
               "name": "name",
               "alias": "alias",
               "is_activated": "is_activated,",
               "host_id": "host.id",
               "host_name": "host.name",
               "hostgroup_id": "hostgroup.id",
               "hostgroup_name": "hostgroup.name",
               "hostcategory_id": "hostcategory.id",
               "hostcategory_name": "hostcategory.name",
               "servicecategory_id": "servicecategory.id",
               "servicecategory_name": "servicecategory.name"})
    def find_service_group_configurations(self,
                                          search: Optional[SearchType] = None,
                                          limit: int = 1000,
                                          page: int = 1,
                                          sort: Optional[Dict[str, Sort]] = None) -> List[ServiceGroupConfigurationList]:
        logger.debug(f"List service groups from {self}.")

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
                                 api_path="/configuration/services/groups",
                                 error_message=f"Could not list host groups from {self}.",
                                 params=params)
        service_groups_dicts = result["result"]

        # parse to ServiceGroupConfigurationList
        service_groups = []
        for service_group_dict in service_groups_dicts:
            service_group = ServiceGroupConfigurationList.model_validate(service_group_dict)
            service_groups.append(service_group)

        logger.debug(f"List service groups from {self} successful. -> {len(service_groups)} service groups")

        return service_groups
