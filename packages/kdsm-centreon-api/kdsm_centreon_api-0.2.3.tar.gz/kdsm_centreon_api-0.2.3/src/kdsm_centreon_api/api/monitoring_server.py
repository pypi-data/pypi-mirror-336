from typing import Optional, Dict, List

from kdsm_centreon_api.api.sub_api import SubApi
from kdsm_centreon_api.api.utils import validate, SearchType, Sort, sort_dump
from kdsm_centreon_api.logger import logger
from kdsm_centreon_api.models.monitoring_server import MonitoringServerList


class MonitoringServer(SubApi):
    @validate({"id": "id",
               "name": "name",
               "is_localhost": "is_localhost",
               "address": "address",
               "is_activate": "is_activate"})
    def list_monitoring_servers(self,
                                search: Optional[SearchType] = None,
                                limit: int = 1000,
                                page: int = 1,
                                sort: Optional[Dict[str, Sort]] = None) -> List[MonitoringServerList]:
        logger.debug(f"List monitoring servers from {self}.")

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
                                 api_path="/configuration/monitoring-servers",
                                 error_message=f"Could not list monitoring servers from {self}.",
                                 params=params)
        monitoring_server_dicts = result["result"]

        # parse to MonitoringServerList
        monitoring_servers = []
        for monitoring_server_dict in monitoring_server_dicts:
            monitoring_server = MonitoringServerList.model_validate(monitoring_server_dict)
            monitoring_servers.append(monitoring_server)

        logger.debug(f"List monitoring servers from {self} successful. -> {len(monitoring_servers)} monitoring servers")

        return monitoring_servers
