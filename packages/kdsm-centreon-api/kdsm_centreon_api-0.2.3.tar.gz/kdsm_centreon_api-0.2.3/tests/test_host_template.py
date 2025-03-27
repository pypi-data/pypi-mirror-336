from kdsm_centreon_api.api.utils import Sort


def test_host_template_list(centreon, test_host_template_name):
    # find existing host template
    exiting_host_templates = centreon.host_template.find_host_templates(name=test_host_template_name, sort={"name": Sort.ASC})
    if len(exiting_host_templates) > 1:
        raise ValueError(f"Multiple host templates with the name '{test_host_template_name}' found.")
    elif len(exiting_host_templates) == 0:
        raise ValueError(f"No host template with the name '{test_host_template_name}' found.")
