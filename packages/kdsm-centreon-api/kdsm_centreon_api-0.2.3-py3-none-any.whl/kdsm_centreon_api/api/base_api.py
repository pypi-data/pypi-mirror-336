from abc import ABC, abstractmethod
from typing import Literal, Optional

from kdsm_centreon_api.api.centreon_version import CentreonVersion


class BaseApi(ABC):
    @property
    @abstractmethod
    def username(self) -> str: ...

    @property
    @abstractmethod
    def password(self) -> str: ...

    @property
    @abstractmethod
    def hostname(self) -> str: ...

    @property
    @abstractmethod
    def port(self) -> int: ...

    @property
    @abstractmethod
    def ssl(self) -> bool: ...

    @property
    @abstractmethod
    def ssl_verify(self) -> bool: ...

    @property
    @abstractmethod
    def ssl_disable_warning(self) -> bool: ...

    @property
    @abstractmethod
    def timeout(self) -> int: ...

    @property
    @abstractmethod
    def api_version(self) -> CentreonVersion: ...

    @property
    @abstractmethod
    def url(self) -> str: ...

    @property
    @abstractmethod
    def api_url_v1(self) -> str: ...

    @property
    @abstractmethod
    def api_url_v2(self) -> str: ...

    @property
    @abstractmethod
    def api_token_v1(self) -> str: ...

    @property
    @abstractmethod
    def api_token_v2(self) -> str: ...

    @abstractmethod
    def request_v1(self,
                   action: str,
                   obj: str,
                   error_message: str,
                   values: Optional[str] = None) -> dict: ...

    @abstractmethod
    def request_v2(self,
                   method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
                   api_path: str,
                   error_message: str,
                   headers: Optional[dict] = None,
                   params: Optional[dict] = None,
                   data: Optional[dict] = None) -> Optional[dict]: ...

    @abstractmethod
    def auth_v1(self) -> str: ...

    @abstractmethod
    def auth_v2(self) -> str: ...

    @abstractmethod
    def logout(self): ...
