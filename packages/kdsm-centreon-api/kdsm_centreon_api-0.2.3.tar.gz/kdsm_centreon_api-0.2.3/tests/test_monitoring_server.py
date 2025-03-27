from kdsm_centreon_api.api.utils import Sort


def test_monitoring_server_list(centreon, test_monitoring_server_name):
    # find existing monitoring server
    exiting_monitoring_server = centreon.monitoring_server.list_monitoring_servers(name=test_monitoring_server_name, sort={"name": Sort.ASC})
    if len(exiting_monitoring_server) > 1:
        raise ValueError(f"Multiple monitoring server with the name '{test_monitoring_server_name}' found.")
    elif len(exiting_monitoring_server) == 0:
        raise ValueError(f"No monitoring server with the name '{test_monitoring_server_name}' found.")
