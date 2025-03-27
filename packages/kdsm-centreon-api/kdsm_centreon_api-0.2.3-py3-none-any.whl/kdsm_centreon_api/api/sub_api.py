from typing import Literal, Optional

from kdsm_centreon_api.api.base_api import BaseApi
from kdsm_centreon_api.api.centreon_version import CentreonVersion


class SubApi(BaseApi):
    def __init__(self, parent_api):
        self._parent_api = parent_api

        # store args and kwargs for __repr__ and __str__
        self.__args__ = (parent_api,)
        self.__kwargs__ = {"parent_api": parent_api}

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.__kwargs__.items()])})"

    def __str__(self):
        return f"{self._parent_api}"

    @property
    def username(self) -> str:
        return self._parent_api.username

    @property
    def password(self) -> str:
        return self._parent_api.password

    @property
    def hostname(self) -> str:
        return self._parent_api.hostname

    @property
    def port(self) -> int:
        return self._parent_api.port

    @property
    def ssl(self) -> bool:
        return self._parent_api.ssl

    @property
    def ssl_verify(self) -> bool:
        return self._parent_api.ssl_verify

    @property
    def ssl_disable_warning(self) -> bool:
        return self._parent_api.ssl_disable_warning

    @property
    def timeout(self) -> int:
        return self._parent_api.timeout

    @property
    def api_version(self) -> CentreonVersion:
        return self._parent_api.api_version

    @property
    def url(self) -> str:
        return self._parent_api.url

    @property
    def api_url_v1(self) -> str:
        return self._parent_api.api_url_v1

    @property
    def api_url_v2(self) -> str:
        return self._parent_api.api_url_v2

    @property
    def api_token_v1(self) -> str:
        return self._parent_api.api_token_v1

    @property
    def api_token_v2(self) -> str:
        return self._parent_api.api_token_v2

    def request_v1(self,
                   action: str,
                   obj: str,
                   error_message: str,
                   values: Optional[str] = None) -> dict:
        return self._parent_api.request_v1(action=action,
                                           obj=obj,
                                           error_message=error_message,
                                           values=values)

    def request_v2(self,
                   method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
                   api_path: str,
                   error_message: str,
                   headers: Optional[dict] = None,
                   params: Optional[dict] = None,
                   data: Optional[dict] = None) -> Optional[dict]:
        return self._parent_api.request_v2(method=method,
                                           api_path=api_path,
                                           error_message=error_message,
                                           headers=headers,
                                           params=params,
                                           data=data)

    def auth_v1(self) -> str:
        return self._parent_api.auth_v1()

    def auth_v2(self) -> str:
        return self._parent_api.auth_v2()

    def logout(self):
        return self._parent_api.logout()
