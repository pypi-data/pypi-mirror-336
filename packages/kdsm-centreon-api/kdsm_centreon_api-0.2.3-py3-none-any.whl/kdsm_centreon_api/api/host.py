from typing import Optional, Dict, List

from kdsm_centreon_api.api.centreon_version import CentreonVersion
from kdsm_centreon_api.api.sub_api import SubApi
from kdsm_centreon_api.api.utils import validate, SearchType, Sort, sort_dump, exclude_on_versions
from kdsm_centreon_api.logger import logger
from kdsm_centreon_api.models.host import HostConfigurationList, HostConfigurationCreate, HostConfigurationCreated, HostRtm


class Host(SubApi):
    @exclude_on_versions(CentreonVersion.v23_04, CentreonVersion.v22_10)
    @validate({"id": "id",
               "name": "name",
               "address": "address",
               "poller_id": "poller.id",
               "poller_name": "poller.name",
               "category_id": "category.id",
               "category_name": "category.name",
               "severity_id": "severity.id",
               "severity_name": "severity.name",
               "group_id": "group.id",
               "group_name": "group.name",
               "is_activated": "is_activated"})
    def find_host_configurations(self,
                                 search: Optional[SearchType] = None,
                                 limit: int = 1000,
                                 page: int = 1,
                                 sort: Optional[Dict[str, Sort]] = None) -> List[HostConfigurationList]:
        logger.debug(f"List hosts from {self}.")

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
                                 api_path="/configuration/hosts",
                                 error_message=f"Could not list hosts from {self}.",
                                 params=params)
        host_dicts = result["result"]

        # parse to HostConfigurationList
        hosts = []
        for host_dict in host_dicts:
            host = HostConfigurationList.model_validate(host_dict)
            hosts.append(host)

        logger.debug(f"List hosts from {self} successful. -> {len(hosts)} hosts")

        return hosts

    @exclude_on_versions(CentreonVersion.v23_04, CentreonVersion.v22_10)
    def create_host_configuration(self, host: HostConfigurationCreate) -> HostConfigurationCreated:
        logger.debug(f"Create host '{host.name}' on {self}.")

        host_dict = host.model_dump(exclude_none=True)

        host_created_dict = self.request_v2(method="POST", api_path="/configuration/hosts", error_message=f"Could not create host '{host.name}' on {self}.", data=host_dict)

        # parse to HostConfigurationCreated
        host_created = HostConfigurationCreated.model_validate(host_created_dict)

        logger.debug(f"Create host '{host_created.name}' on {self} successful.")

        return host_created

    @exclude_on_versions(CentreonVersion.v23_10, CentreonVersion.v23_04, CentreonVersion.v22_10)
    def update_host_configuration(self, host_id: int, host: HostConfigurationCreate) -> None:
        logger.debug(f"Update host '{host_id}' on {self}.")

        host_dict = host.model_dump(exclude_unset=True)
        host_dict["macros"] = [macro.model_dump() for macro in host.macros]

        self.request_v2(method="PATCH",
                        api_path=f"/configuration/hosts/{host_id}",
                        error_message=f"Could not update host '{host_id}' on {self}.",
                        data=host_dict)

        logger.debug(f"Update host '{host_id}' on {self} successful.")

        return None

    def apply_host_configuration(self, host_name: str) -> None:
        logger.debug(f"Apply host '{host_name}' on {self}.")

        self.request_v1(action="applytpl", obj="host", error_message=f"Could not apply host '{host_name}' on {self}.", values=host_name)

    @exclude_on_versions(CentreonVersion.v23_04, CentreonVersion.v22_10)
    def delete_host_configuration(self, host_id: int) -> None:
        logger.debug(f"Delete host '{host_id}' from {self}.")

        self.request_v2(method="DELETE", api_path=f"/configuration/hosts/{host_id}", error_message=f"Could not delete host '{host_id}' from {self}.")

        logger.debug(f"Delete host '{host_id}' from {self} successful.")

    @validate({"host_id": "host.id",
               "host_name": "host.name",
               "host_alias": "host.alias",
               "host_address": "host.address",
               "host_state": "host.state",
               "poller_id": "poller.id",
               "service_display_name": "service.display_name",
               "host_group_id": "host_group.id",
               "host_is_acknowledged": "host.is_acknowledged",
               "host_downtime": "host.downtime",
               "host_criticality": "host.criticality"})
    def list_hosts(self,
                   search: Optional[SearchType] = None,
                   limit: int = 1000,
                   page: int = 1,
                   sort: Optional[Dict[str, Sort]] = None,
                   show_service: bool = False) -> List[HostRtm]:
        logger.debug(f"List hosts from {self}.")

        # params
        params = {
            "show_service": show_service,
            "search": search.dump(),
            "limit": limit,
            "page": page
        }

        if sort is not None:
            # dump sort
            params["sort_by"] = sort_dump(sort)

        result = self.request_v2(method="GET",
                                 api_path="/monitoring/hosts",
                                 error_message=f"Could not list hosts from {self}.",
                                 params=params)
        host_dicts = result["result"]

        # parse to HostRtm
        hosts = []
        for host_dict in host_dicts:
            host = HostRtm.model_validate(host_dict)
            hosts.append(host)

        logger.debug(f"List hosts from {self} successful. -> {len(hosts)} hosts")

        return hosts
