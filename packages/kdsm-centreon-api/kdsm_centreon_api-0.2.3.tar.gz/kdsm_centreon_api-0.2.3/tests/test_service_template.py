from tests.conftest import skip_versions, CentreonVersion

from kdsm_centreon_api.api.utils import And, Sort


@skip_versions(CentreonVersion.v23_04, CentreonVersion.v22_10)
def test_service_template_list(centreon, test_service_template_name):
    if centreon.api_version != CentreonVersion.v24_04.value:
        # find existing service template
        exiting_service_templates = centreon.service_template.find_service_templates(And(name=test_service_template_name), 123, 1, sort={"name": Sort.ASC})
        if len(exiting_service_templates) > 1:
            raise ValueError(f"Multiple service templates with the name '{test_service_template_name}' found.")
        elif len(exiting_service_templates) == 0:
            raise ValueError(f"No service template with the name '{test_service_template_name}' found.")
    else:
        # ToDo: currently not working, i think its a problem with the api, again .....
        # find existing service template
        exiting_service_templates = centreon.service_template.find_service_templates(limit=123, page=1, sort={"name": Sort.ASC})
        found_service_template = False
        for service_template in exiting_service_templates:
            if service_template.name == test_service_template_name:
                found_service_template = True
                break
        if not found_service_template:
            raise ValueError(f"No service template with the name '{test_service_template_name}' found.")
