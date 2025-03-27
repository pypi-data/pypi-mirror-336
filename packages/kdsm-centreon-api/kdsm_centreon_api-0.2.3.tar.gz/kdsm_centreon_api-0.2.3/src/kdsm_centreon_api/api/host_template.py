from typing import Optional, Dict, List

from kdsm_centreon_api.api.sub_api import SubApi
from kdsm_centreon_api.api.utils import validate, SearchType, Sort, sort_dump
from kdsm_centreon_api.logger import logger
from kdsm_centreon_api.models.host_template import HostTemplateList


class HostTemplate(SubApi):
    @validate({"id": "id",
               "name": "name",
               "alias": "alias",
               "is_locked": "is_locked"})
    def find_host_templates(self,
                            search: Optional[SearchType] = None,
                            limit: int = 1000,
                            page: int = 1,
                            sort: Optional[Dict[str, Sort]] = None) -> List[HostTemplateList]:
        logger.debug(f"List host templates from {self}.")

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
                                 api_path="/configuration/hosts/templates",
                                 error_message=f"Could not list host templates from {self}.",
                                 params=params)
        host_template_dicts = result["result"]

        # parse to HostGroupList
        host_templates = []
        for host_template_dict in host_template_dicts:
            host_template = HostTemplateList.model_validate(host_template_dict)
            host_templates.append(host_template)

        logger.debug(f"List host templates from {self} successful. -> {len(host_templates)} host templates")

        return host_templates
