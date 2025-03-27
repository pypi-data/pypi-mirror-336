import json
import urllib.parse
from typing import Literal, Optional

import requests

from kdsm_centreon_api.api.centreon_version import CentreonVersion
from kdsm_centreon_api.api.base_api import BaseApi
from kdsm_centreon_api.api.host import Host
from kdsm_centreon_api.api.host_group import HostGroup
from kdsm_centreon_api.api.host_template import HostTemplate
from kdsm_centreon_api.api.monitoring_server import MonitoringServer
from kdsm_centreon_api.api.service import Service
from kdsm_centreon_api.api.service_group import ServiceGroup
from kdsm_centreon_api.api.service_template import ServiceTemplate
from kdsm_centreon_api.api.utils import disable_insecure_request_warning
from kdsm_centreon_api.logger import logger


class Centreon(BaseApi):
    def __init__(self,
                 hostname: str = "localhost",
                 port: int = 443,
                 username: str = "admin",
                 password: str = "password",
                 ssl: Optional[bool] = None,
                 ssl_verify: bool = True,
                 ssl_disable_warning: bool = False,
                 timeout: int = 10,
                 api_version: CentreonVersion = CentreonVersion.LATEST):
        # set args
        self._hostname = hostname
        self._port = port
        self._username = username
        self._password = password
        if ssl is None:
            ssl = port == 443
        self._ssl = ssl
        self._ssl_verify = ssl_verify
        self._ssl_disable_warning = ssl_disable_warning
        self._timeout = timeout
        self._api_version = api_version

        # store args and kwargs for __repr__ and __str__
        self.__args__ = (hostname, port, username, password, ssl, ssl_verify, timeout, api_version)
        self.__kwargs__ = {
            "hostname": self.hostname,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "ssl": self.ssl,
            "ssl_verify": self.ssl_verify,
            "timeout": self.timeout,
            "api_version": self.api_version
        }

        # get url
        if self.ssl:
            with disable_insecure_request_warning(self.ssl_disable_warning):
                response = requests.get("https://" + self.hostname + ":" + str(self.port), verify=self.ssl_verify, timeout=self.timeout)
        else:
            response = requests.get("http://" + self.hostname + ":" + str(self.port), verify=self.ssl_verify, timeout=self.timeout)
        if not response.ok:
            raise requests.exceptions.RequestException(f"Could not get url -> {response.status_code} {response.reason}")
        url_parsed = urllib.parse.urlparse(response.url)
        port = url_parsed.port if url_parsed.port else self.port
        self._url = url_parsed.scheme + "://" + url_parsed.netloc + ":" + str(port) + url_parsed.path

        # define api urls
        self._api_url_v1 = f"{self._url}api/index.php"
        self._api_url_v2 = f"{self._url}api/{self.api_version.value}"

        # define api tokens
        self._api_token_v1: Optional[str] = None
        self._api_token_v2: Optional[str] = None

        logger.debug(f"Create {self}.")

        # define sub apis
        self.monitoring_server: MonitoringServer = MonitoringServer(self)
        self.host: Host = Host(self)
        self.host_group: HostGroup = HostGroup(self)
        self.host_template: HostTemplate = HostTemplate(self)
        self.service: Service = Service(self)
        self.service_group: ServiceGroup = ServiceGroup(self)
        self.service_template: ServiceTemplate = ServiceTemplate(self)

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.__kwargs__.items()])})"

    def __str__(self):
        return f"{self.__class__.__name__}(host={self.hostname}, port={self.port})"

    def __del__(self):
        if self._api_token_v2 is not None:
            try:
                self.logout()
            except ImportError:
                ...

    def __enter__(self) -> "Centreon":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._api_token_v2 is not None:
            self.logout()

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:

        return self._password

    @property
    def hostname(self) -> str:
        return self._hostname

    @property
    def port(self) -> int:
        return self._port

    @property
    def ssl(self) -> bool:
        return self._ssl

    @property
    def ssl_verify(self) -> bool:
        return self._ssl_verify

    @property
    def ssl_disable_warning(self) -> bool:
        return self._ssl_disable_warning

    @property
    def timeout(self) -> int:
        return self._timeout

    @property
    def api_version(self) -> CentreonVersion:
        return self._api_version

    @property
    def url(self) -> str:
        return self._url

    @property
    def api_url_v1(self) -> str:
        return self._api_url_v1

    @property
    def api_url_v2(self) -> str:
        return self._api_url_v2

    @property
    def api_token_v1(self) -> str:
        if self._api_token_v1 is None:
            logger.debug(f"Get API v1 token from {self}.")

            self._api_token_v1 = self.auth_v1()

        return self._api_token_v1

    @property
    def api_token_v2(self) -> str:
        if self._api_token_v2 is None:
            logger.debug(f"Get API v2 token from {self}.")

            self._api_token_v2 = self.auth_v2()

        return self._api_token_v2

    def request_v1(self,
                   action: str,
                   obj: str,
                   error_message: str,
                   values: Optional[str] = None) -> dict:

        headers = {
            "Content-Type": "application/json",
            "centreon-auth-token": self.api_token_v1
        }

        params = {
            "action": "action",
            "object": "centreon_clapi"
        }

        data = {
            "action": action,
            "object": obj
        }

        if values is not None:
            data["values"] = values

        data_str = json.dumps(data)

        logger.debug(f"Request {action} {obj} from {self}.")

        with disable_insecure_request_warning(self.ssl_disable_warning):
            result = requests.post(self.api_url_v1,
                                   headers=headers,
                                   params=params,
                                   data=data_str,
                                   verify=self.ssl_verify,
                                   timeout=self.timeout)

        if not result.ok:
            raise requests.exceptions.RequestException(f"{error_message} -> {result.status_code} {result.reason}")

        result_json = result.json()

        return result_json

    def request_v2(self,
                   method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
                   api_path: str,
                   error_message: str,
                   headers: Optional[dict] = None,
                   params: Optional[dict] = None,
                   data: Optional[dict] = None) -> Optional[dict]:

        full_url = f"{self.api_url_v2}{api_path}"

        if headers is None:
            headers = {}

        headers["X-AUTH-TOKEN"] = self.api_token_v2

        if data is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(data)

        logger.debug(f"Request {method} {full_url}.")

        with disable_insecure_request_warning(self.ssl_disable_warning):
            response = requests.request(method,
                                        full_url,
                                        headers=headers,
                                        params=params,
                                        data=data,
                                        verify=self.ssl_verify,
                                        timeout=self.timeout)

        if not response.ok:
            code = response.status_code
            reason = response.reason
            try:
                result = response.json()
                code = result["code"]
                reason = result["message"]
            except json.JSONDecodeError:
                pass
            raise requests.exceptions.RequestException(f"{error_message} -> {code} {reason}")

        # try to get json from response
        result = None
        try:
            result = response.json()
        except json.JSONDecodeError:
            pass

        return result

    def auth_v1(self) -> str:
        logger.debug(f"Auth to {self} v1.")

        with disable_insecure_request_warning(self.ssl_disable_warning):
            result = requests.post(self.api_url_v1,
                                   headers={
                                       "Content-Type": "application/x-www-form-urlencoded"
                                   },
                                   params={
                                       "action": "authenticate"
                                   },
                                   data={
                                       "username": self.username,
                                       "password": self.password
                                   },
                                   verify=self.ssl_verify,
                                   timeout=self.timeout)

        if not result.ok:
            raise requests.exceptions.RequestException(f"Could not auth to {self} v1. -> {result.status_code} {result.reason}")

        v1_token = result.json()["authToken"]

        logger.debug(f"Auth to {self} v1 successful. -> token={v1_token}")

        return v1_token

    def auth_v2(self) -> str:
        logger.debug(f"Auth to {self} v2.")

        with disable_insecure_request_warning(self.ssl_disable_warning):
            response = requests.request("POST",
                                        f"{self.api_url_v2}/login",
                                        headers={
                                            "Content-Type": "application/json"
                                        },
                                        data=json.dumps({
                                            "security": {
                                                "credentials": {
                                                    "login": self.username,
                                                    "password": self.password
                                                }
                                            }
                                        }),
                                        verify=self.ssl_verify,
                                        timeout=self.timeout)

        if not response.ok:
            raise requests.exceptions.RequestException(f"Could not auth to {self}. -> {response.status_code} {response.reason}")

        # get token
        token = response.json()["security"]["token"]

        logger.debug(f"Auth to {self} v2 successful. -> token={token}")

        return token

    def logout(self):
        logger.debug(f"Logout from {self}.")

        self.request_v2(method="GET", api_path="/logout", error_message=f"Could not logout from {self}.")

        self._api_token_v1 = None
        self._api_token_v2 = None

        logger.debug(f"Logout from {self} successful.")
