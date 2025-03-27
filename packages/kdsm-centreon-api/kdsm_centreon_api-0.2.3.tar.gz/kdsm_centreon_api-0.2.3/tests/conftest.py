from functools import wraps
from pathlib import Path

import pytest
import toml
import urllib3

from kdsm_centreon_api.api.centreon import Centreon
from kdsm_centreon_api.api.centreon_version import CentreonVersion
from kdsm_centreon_api.api.sub_api import SubApi

from typing import List, Tuple


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="all", help="Environment to run tests in")


def pytest_generate_tests(metafunc):
    # get current environment
    env = metafunc.config.getoption("--env")

    # get pyproject.toml
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    if not pyproject_path.is_file():
        raise FileNotFoundError("pyproject.toml not found")
    pyproject = toml.load(pyproject_path)

    environments: List[Tuple[CentreonVersion, dict]] = []
    if env == "all":
        for env_version_name, env_config in pyproject["tool"]["pytest"]["env"].items():
            # get CentreonVersion object
            version = getattr(CentreonVersion, env_version_name)

            # add environment to list
            environments.append((version, env_config))
    else:
        # check if environments are defined in pyproject.toml
        if "env" not in pyproject["tool"]["pytest"]:
            raise KeyError("No environments found in pyproject.toml")
        if env not in pyproject["tool"]["pytest"]["env"]:
            raise ValueError(f"Environment '{env}' not found in pyproject.toml")

        # get CentreonVersion object
        version = getattr(CentreonVersion, env)

        # add environment to list
        environments.append((version, pyproject["tool"]["pytest"]["env"][env]))

    if "environment" in metafunc.fixturenames:
        metafunc.parametrize("environment", environments, ids=[f"{version.name}" for version, _ in environments])


def skip_versions(*versions):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # get centreon object
            api: SubApi = kwargs.get("centreon")

            # check if version is valid
            for version in versions:
                if api.api_version == version:
                    pytest.skip(f"skipping test for version {api.api_version}")

            return func(*args, **kwargs)

        return wrapper

    return decorator


@pytest.fixture()
def centreon(environment):
    version, environment = environment
    return Centreon(
        hostname=environment["hostname"],
        port=environment["port"],
        username=environment["username"],
        password=environment["password"],
        ssl=environment["ssl"],
        ssl_verify=environment["ssl_verify"],
        ssl_disable_warning=True,
        api_version=version
    )


@pytest.fixture()
def centreon_disabled_warnings(environment):
    version, environment = environment
    urllib3.disable_warnings()
    return Centreon(
        hostname=environment["hostname"],
        port=environment["port"],
        username=environment["username"],
        password=environment["password"],
        ssl=environment["ssl"],
        ssl_verify=environment["ssl_verify"],
        api_version=version
    )


@pytest.fixture()
def test_command_id(centreon) -> int:
    return 91


@pytest.fixture()
def test_icon_id(centreon) -> int:
    return 1


@pytest.fixture()
def test_severity_id(centreon) -> int:
    return 1


@pytest.fixture()
def test_monitoring_server_name(centreon) -> str:
    return "Central"


@pytest.fixture()
def test_monitoring_server_id(centreon, test_monitoring_server_name) -> int:
    test_monitoring_server = centreon.monitoring_server.list_monitoring_servers(name=test_monitoring_server_name)
    if len(test_monitoring_server) == 0:
        raise ValueError(f"No monitoring server with the name '{test_monitoring_server_name}' found.")
    elif len(test_monitoring_server) > 1:
        raise ValueError(f"Multiple monitoring servers with the name '{test_monitoring_server_name}' found.")
    return test_monitoring_server[0].id


@pytest.fixture()
def test_host_name(centreon) -> str:
    return "kdsm_centreon_api_test_host"


@pytest.fixture()
def test_host_name_rt_name(centreon) -> str:
    return "kdsm_centreon_api_test_host_rt"


@pytest.fixture()
def test_host_name_rt_id(centreon, test_host_name_rt_name) -> int:
    test_host = centreon.host.list_hosts(host_name=test_host_name_rt_name)
    if len(test_host) == 0:
        raise ValueError(f"No host with the name '{test_host_name_rt_name}' found.")
    elif len(test_host) > 1:
        raise ValueError(f"Multiple hosts with the name '{test_host_name_rt_name}' found.")
    return test_host[0].id


@pytest.fixture()
def test_host_group_name(centreon) -> str:
    return "kdsm_centreon_api_test_host_group"


@pytest.fixture()
def test_host_group_rt_name(centreon) -> str:
    return "kdsm_centreon_api_test_host_group_rt"


@pytest.fixture()
def test_host_group_rt_id(centreon, test_host_group_rt_name) -> int:
    test_host_group = centreon.host_group.find_host_group_configurations(name=test_host_group_rt_name)
    if len(test_host_group) == 0:
        raise ValueError(f"No host group with the name '{test_host_group_rt_name}' found.")
    elif len(test_host_group) > 1:
        raise ValueError(f"Multiple host groups with the name '{test_host_group_rt_name}' found.")
    return test_host_group[0].id


@pytest.fixture()
def test_host_template_name(centreon) -> str:
    return "kdsm_centreon_api_test_host_template"


@pytest.fixture()
def test_host_template_id(centreon, test_host_template_name) -> int:
    test_host_template = centreon.host_template.find_host_templates(name=test_host_template_name)
    if len(test_host_template) == 0:
        raise ValueError(f"No host template with the name '{test_host_template_name}' found.")
    elif len(test_host_template) > 1:
        raise ValueError(f"Multiple host templates with the name '{test_host_template_name}' found.")
    return test_host_template[0].id


@pytest.fixture()
def test_service_name(centreon) -> str:
    return "kdsm_centreon_api_test_service"


@pytest.fixture()
def test_service_name_rt_name(centreon) -> str:
    return "kdsm_centreon_api_test_service_rt"


@pytest.fixture()
def test_service_template_name(centreon) -> str:
    return "kdsm_centreon_api_test_service_template"


@pytest.fixture()
@skip_versions(CentreonVersion.v23_04, CentreonVersion.v22_10)
def test_service_template_id(centreon, test_service_template_name) -> int:
    # ToDo: currently not working, i think its a problem with the api, again .....
    test_service_template = centreon.service_template.find_service_templates()
    for service_template in test_service_template:
        if service_template.name == test_service_template_name:
            return service_template.id
    raise ValueError(f"No service template with the name '{test_service_template_name}' found.")

    # if len(test_service_template) == 0:
    #     raise ValueError(f"No service template with the name '{test_service_template_name}' found.")
    # elif len(test_service_template) > 1:
    #     raise ValueError(f"Multiple service templates with the name '{test_service_template_name}' found.")
    # return test_service_template[0].id


@pytest.fixture()
def test_service_group_name(centreon) -> str:
    return "kdsm_centreon_api_test_service_group"


@pytest.fixture()
def test_service_group_rt_name(centreon) -> str:
    return "kdsm_centreon_api_test_service_group_rt"


@pytest.fixture()
@skip_versions(CentreonVersion.v22_10)
def test_service_group_rt_id(centreon, test_service_group_rt_name) -> int:
    test_service_group = centreon.service_group.find_service_group_configurations(name=test_service_group_rt_name)
    if len(test_service_group) == 0:
        raise ValueError(f"No service group with the name '{test_service_group_rt_name}' found.")
    elif len(test_service_group) > 1:
        raise ValueError(f"Multiple service groups with the name '{test_service_group_rt_name}' found.")
    return test_service_group[0].id
