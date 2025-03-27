from typing import Optional, Dict, List

from kdsm_centreon_api.api.centreon_version import CentreonVersion
from kdsm_centreon_api.api.sub_api import SubApi
from kdsm_centreon_api.api.utils import validate, SearchType, Sort, sort_dump, exclude_on_versions
from kdsm_centreon_api.logger import logger
from kdsm_centreon_api.models.service_template import ServiceTemplateList


class ServiceTemplate(SubApi):
    @exclude_on_versions(CentreonVersion.v23_04, CentreonVersion.v22_10)
    @validate({"id": "id",
               "name": "name",
               "alias": "alias",
               "is_locked": "is_locked"})
    def find_service_templates(self,
                               search: Optional[SearchType] = None,
                               limit: int = 1000,
                               page: int = 1,
                               sort: Optional[Dict[str, Sort]] = None) -> List[ServiceTemplateList]:
        logger.debug(f"List service templates from {self}.")

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
                                 api_path="/configuration/services/templates",
                                 error_message=f"Could not list service templates from {self}.",
                                 params=params)
        service_template_dicts = result["result"]

        # parse to ServiceTemplateList
        service_templates = []
        for service_template_dict in service_template_dicts:
            service_template = ServiceTemplateList.model_validate(service_template_dict)
            service_templates.append(service_template)

        logger.debug(f"List service templates from {self} successful. -> {len(service_templates)} service templates")

        return service_templates
