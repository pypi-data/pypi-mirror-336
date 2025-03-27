from typing import Optional, Dict, List

from kdsm_centreon_api.api.centreon_version import CentreonVersion
from kdsm_centreon_api.api.sub_api import SubApi
from kdsm_centreon_api.api.utils import validate, SearchType, Sort, sort_dump, exclude_on_versions
from kdsm_centreon_api.logger import logger
from kdsm_centreon_api.models.service import ServiceConfigurationList, ServiceConfigurationCreated, ServiceConfigurationCreate, ServiceRtm


class Service(SubApi):
    @exclude_on_versions(CentreonVersion.v23_04, CentreonVersion.v22_10)
    @validate({"name": "name",
               "host_id": "host.id",
               "host_name": "host.name",
               "category_id": "category.id",
               "category_name": "category.name",
               "severity_id": "severity.id",
               "severity_name": "severity.name",
               "group_id": "group.id",
               "group_name": "group.name",
               "hostgroup_id": "hostgroup.id",
               "hostgroup_name": "hostgroup.name",
               "hostcategory_id": "hostcategory.id",
               "hostcategory_name": "hostcategory.name"})
    def find_service_configurations(self,
                                    search: Optional[SearchType] = None,
                                    limit: int = 1000,
                                    page: int = 1,
                                    sort: Optional[Dict[str, Sort]] = None) -> List[ServiceConfigurationList]:
        logger.debug(f"List services from {self}.")

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
                                 api_path="/configuration/services",
                                 error_message=f"Could not list services from {self}.",
                                 params=params)
        service_dicts = result["result"]

        # parse to ServiceConfigurationList
        services = []
        for service_dict in service_dicts:
            service = ServiceConfigurationList.model_validate(service_dict)
            services.append(service)

        logger.debug(f"List services from {self} successful. -> {len(services)} hosts")

        return services

    @exclude_on_versions(CentreonVersion.v23_04, CentreonVersion.v22_10)
    def create_service_configuration(self, service: ServiceConfigurationCreate) -> ServiceConfigurationCreated:
        logger.debug(f"Create service '{service.name}' on {self}.")

        service_dict = service.model_dump(exclude_none=True)

        service_created_dict = self.request_v2(method="POST", api_path="/configuration/services", error_message=f"Could not create service '{service.name}' on {self}.",
                                               data=service_dict)

        # parse to ServiceConfigurationCreated
        service_created = ServiceConfigurationCreated.model_validate(service_created_dict)

        logger.debug(f"Create service '{service_created.name}' on {self} successful.")

        return service_created

    @exclude_on_versions(CentreonVersion.v23_10, CentreonVersion.v23_04, CentreonVersion.v22_10)
    def update_service_configuration(self, service_id: int, service: ServiceConfigurationCreate) -> None:
        logger.debug(f"Update service '{service_id}' on {self}.")

        service_dict = service.model_dump(exclude_unset=True)
        service_dict["macros"] = [macro.model_dump() for macro in service.macros]

        self.request_v2(method="PATCH", api_path=f"/configuration/services/{service_id}", error_message=f"Could not update service '{service_id}' on {self}.",
                        data=service_dict)

        logger.debug(f"Update service '{service_id}' on {self} successful.")

        return None

    @exclude_on_versions([CentreonVersion.v23_04, CentreonVersion.v22_10])
    def delete_service_configuration(self, service_id: int) -> dict:
        logger.debug(f"Delete service '{service_id}' from {self}.")

        result = self.request_v2(method="DELETE", api_path=f"/configuration/services/{service_id}", error_message=f"Could not delete service '{service_id}' from {self}.")

        logger.debug(f"Delete service '{service_id}' from {self} successful.")

        return result

    @validate({"service_id": "service.id",
               "service_description": "service.description",
               "service_display_name": "service.display_name",
               "service_group_id": "service_group.id",
               "service_group_name": "service_group.name",
               "service_state": "service.state"})
    def get_service_related_to_host(self,
                                    host_id: int,
                                    search: Optional[SearchType] = None,
                                    limit: int = 1000,
                                    page: int = 1,
                                    sort: Optional[Dict[str, Sort]] = None) -> List[ServiceRtm]:
        logger.debug(f"Get services related to host '{host_id}' from {self}.")

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
                                 api_path=f"/monitoring/hosts/{host_id}/services",
                                 error_message=f"Could not get services related to host '{host_id}' from {self}.",
                                 params=params)

        services_rtm_dict = result["result"]

        # parse to ServiceRtl
        services_rtm = []
        for service_rtm_dict in services_rtm_dict:
            service_rtm = ServiceRtm.model_validate(service_rtm_dict)
            services_rtm.append(service_rtm)

        logger.debug(f"Get services related to host '{host_id}' from {self} successful. -> {len(services_rtm)} services")

        return services_rtm
