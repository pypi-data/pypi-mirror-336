import pytest
import requests


def test_repr(centreon):
    centreon_repr_test = f"{centreon.__class__.__name__}({', '.join([f'{k}={v}' for k, v in centreon.__kwargs__.items()])})"
    assert repr(centreon) == centreon_repr_test


def test_sub_api(centreon):
    assert centreon.username is centreon.host.username
    assert centreon.password is centreon.host.password
    assert centreon.hostname is centreon.host.hostname
    assert centreon.port is centreon.host.port
    assert centreon.ssl is centreon.host.ssl
    assert centreon.ssl_verify is centreon.host.ssl_verify
    assert centreon.ssl_disable_warning is centreon.host.ssl_disable_warning
    assert centreon.timeout is centreon.host.timeout
    assert centreon.api_version is centreon.host.api_version
    assert centreon.url is centreon.host.url
    assert centreon.api_url_v1 is centreon.host.api_url_v1
    assert centreon.api_url_v2 is centreon.host.api_url_v2
    assert centreon.api_token_v1 is centreon.host.api_token_v1
    assert centreon.api_token_v2 is centreon.host.api_token_v2

    centreon_host_repr_test = f"{centreon.host.__class__.__name__}({', '.join([f'{k}={v}' for k, v in centreon.host.__kwargs__.items()])})"
    assert repr(centreon.host) == centreon_host_repr_test


def test_bad_request(centreon):
    with pytest.raises(requests.exceptions.RequestException):
        centreon.request_v1("GET", "/api/bad_request", error_message="error_message")
    with pytest.raises(requests.exceptions.RequestException):
        centreon.request_v2("GET", "/api/bad_request", error_message="error_message")


def test_auth(centreon, centreon_disabled_warnings):
    centreon.auth_v1()
    centreon.host.auth_v1()
    centreon.auth_v2()
    centreon.host.auth_v2()
    centreon_disabled_warnings.auth_v1()
    centreon_disabled_warnings.host.auth_v1()
    centreon_disabled_warnings.auth_v2()
    centreon_disabled_warnings.host.auth_v2()


def test_logout(centreon, centreon_disabled_warnings):
    centreon.logout()
    centreon.host.logout()
    centreon_disabled_warnings.logout()
    centreon_disabled_warnings.host.logout()
