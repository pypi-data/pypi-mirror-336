import contextlib
import inspect
import warnings
from copy import deepcopy
from enum import Enum
from functools import wraps
from typing import TypeVar, Any, List, Optional, Tuple, Dict, Union

import urllib3

from kdsm_centreon_api.api.sub_api import SubApi


def exclude_on_versions(*versions):
    def decorator(func):
        @wraps(func)
        def wrapper(self: SubApi, *args, **kwargs):
            # check if version is valid
            for version in versions:
                if self.api_version == version:
                    raise ValueError(f"Function '{func.__name__}' is not available on version '{self.api_version}'.")

            return func(self, *args, **kwargs)

        return wrapper

    return decorator


@contextlib.contextmanager
def disable_insecure_request_warning(disable: bool = True):
    # get current filters
    current_filters = deepcopy(warnings.filters)
    try:
        # disable warning
        if disable:
            warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)
        yield
    finally:
        # reset filters
        if disable:
            warnings.filters = current_filters


class _CompareOperator:
    op: Optional[str] = None
    value_types: Optional[Tuple[type]] = None

    def __init__(self, value: Any):
        if self.op is None:
            raise ValueError(f"Operator must be set for {self.__class__.__name__}.")
        self.key: Optional[str] = None
        if self.value_types is None:
            raise ValueError(f"Value types must be set for {self.__class__.__name__}.")
        else:
            if not isinstance(value, self.value_types):
                raise ValueError(f"Value must be of type {self.value_types}, not {type(value)}")
        self.value = value

    def __str__(self):
        separator = "\"" if type(self.value) is str else ""
        return f'{self.__class__.__name__}({separator}{self.value}{separator})'

    def dict(self) -> Dict[str, Dict[str, Any]]:
        # check if key is set
        if self.key is None:
            raise ValueError(f"Key must be set for {self.__class__.__name__}.")

        # convert value to string if it is not a string
        if type(self.value) is bool:
            self.value = str(self.value).lower()
        if type(self.value) is float or type(self.value) is int:
            self.value = str(self.value)

        return {self.key: {self.op: self.value}}


class Equal(_CompareOperator):
    op = "$eq"
    value_types = (str, int, float, bool)

    def __init__(self, value: Union[str, int, float, bool]):
        super().__init__(value=value)


class NotEqual(_CompareOperator):
    op = "$ne"
    value_types = (str, int, float, bool)

    def __init__(self, value: Union[str, int, float, bool]):
        super().__init__(value=value)


class LessThan(_CompareOperator):
    op = "$lt"
    value_types = (str, int, float)

    def __init__(self, value: Union[str, int, float]):
        super().__init__(value=value)


class LessThanOrEqual(_CompareOperator):
    op = "$le"
    value_types = (str, int, float)

    def __init__(self, value: Union[str, int, float]):
        super().__init__(value=value)


class GreaterThan(_CompareOperator):
    op = "$gt"
    value_types = (str, int, float)

    def __init__(self, value: Union[str, int, float]):
        super().__init__(value=value)


class GreaterThanOrEqual(_CompareOperator):
    op = "$ge"
    value_types = (str, int, float)

    def __init__(self, value: Union[str, int, float]):
        super().__init__(value=value)


class Like(_CompareOperator):
    op = "$lk"
    value_types = (str,)

    def __init__(self, value: str):
        super().__init__(value=value)


class NotLike(_CompareOperator):
    op = "$nk"
    value_types = (str,)

    def __init__(self, value: str):
        super().__init__(value=value)


class In(_CompareOperator):
    op = "$in"
    value_types = (list,)

    def __init__(self, value: List[str]):
        super().__init__(value=value)


class NotIn(_CompareOperator):
    op = "$ni"
    value_types = (list,)

    def __init__(self, value: List[str]):
        super().__init__(value=value)


class Regex(_CompareOperator):
    op = "$rg"
    value_types = (str,)

    def __init__(self, value: str):
        super().__init__(value=value)


CompareType = TypeVar("CompareType", Equal, NotEqual, LessThan, LessThanOrEqual, GreaterThan, GreaterThanOrEqual, Like, NotLike, In, NotIn, Regex)


class _Search:
    key = None

    def __init__(self, *args: "SearchType", **kwargs: Union[str, CompareType]):
        self.args: List["SearchType"] = [*args]

        # convert kwargs values with type str to Equal
        for k, compare in kwargs.items():
            if not isinstance(compare, _CompareOperator):
                compare = Equal(value=compare)
            compare.key = k
            kwargs[k] = compare

        self.kwargs: Dict[str, CompareType] = kwargs

    def __str__(self):
        args_str = ", ".join([str(arg) for arg in self.args])
        kwargs_str = ", ".join([f'{k}="{v}"' for k, v in self.kwargs.items()])
        full_str = ""
        if args_str:
            full_str += args_str
        if kwargs_str:
            if args_str:
                full_str += ", "
            full_str += kwargs_str
        return f"{self.__class__.__name__}({full_str})"

    def __len__(self) -> int:
        length = len(self.args) + len(self.kwargs)
        return length

    def dict(self) -> Dict[str, List[Dict[str, Any]]]:
        if len(self) == 0:
            return {}
        self_dict = {self.key: []}
        for arg in self.args:
            self_dict[self.key].append(arg.dict())
        for compare in self.kwargs.values():
            self_dict[self.key].append(compare.dict())
        return self_dict

    def dump(self) -> str:
        if len(self) == 0:
            return ""
        return str(self.dict()).replace("'", "\"")


class Or(_Search):
    key = "$or"


class And(_Search):
    key = "$and"


SearchType = TypeVar("SearchType", Or, And)


class Sort(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


def sort_dump(sort: Dict[str, Sort]) -> str:
    return str({k: v.value for k, v in sort.items()}).replace("'", "\"")


def validate(key_map: Dict[str, str]):
    def decorator(func):
        func_signature = inspect.signature(func)

        @wraps(func)
        def wrapper(*args,
                    # search: SearchType | None = None,
                    # limit: int | None = None,
                    # page: int | None = None,
                    # sort: dict[str, Sort] | None = None,
                    **kwargs: Union[str, CompareType]):
            # get search kwargs
            search_kwargs = {}
            for key, value in kwargs.items():
                if key in key_map:
                    search_kwargs[key] = value
            for key in search_kwargs.keys():
                del kwargs[key]

            # get bound arguments
            try:
                bound_arguments = func_signature.bind(*args, **kwargs)
            except TypeError as e:
                msg = str(e)
                if "got an unexpected keyword argument" in msg:
                    param_name = msg.split("'")[1].strip()
                    raise ValueError(f"Key '{param_name}' is not allowed in search. Allowed keys are: {', '.join(key_map.keys())}")
                else:
                    raise e
            self = bound_arguments.arguments["self"]
            search = bound_arguments.arguments.get("search")
            if "search" in kwargs:
                del kwargs["search"]
            limit = bound_arguments.arguments.get("limit")
            if "limit" in kwargs:
                del kwargs["limit"]
            page = bound_arguments.arguments.get("page")
            if "page" in kwargs:
                del kwargs["page"]
            sort = bound_arguments.arguments.get("sort")
            if "sort" in kwargs:
                del kwargs["sort"]

            # validate self
            if not isinstance(self, SubApi):
                raise ValueError("self must be an instance of SubApi")

            # validate search
            if search is not None:
                if len(kwargs) > 0:
                    raise ValueError("Either 'search' or 'kwargs' must be set, not both.")
            else:
                search = And(**search_kwargs)

            def translate_key(s: SearchType) -> SearchType:
                for i, arg in enumerate(s.args):
                    if isinstance(arg, And) or isinstance(arg, Or):
                        s.args[i] = translate_key(arg)
                    else:
                        raise ValueError("Only And and Or are allowed as arguments.")
                new_kwargs = {}
                for k, c in s.kwargs.items():
                    if k in key_map:
                        new_k = key_map[k]
                        c.key = new_k
                        new_kwargs[new_k] = c
                    else:
                        raise ValueError(f"Key '{k}' is not allowed in '{s}'. Allowed keys are: {', '.join(key_map.keys())}")
                s.kwargs = new_kwargs
                return s

            # translate keys in search
            search = translate_key(search)

            # validate limit
            if limit is not None:
                if not isinstance(limit, int):
                    raise ValueError("limit must be an integer")
                if limit < 1:
                    raise ValueError("limit must be greater than 0")

            # validate page
            if page is not None:
                if not isinstance(page, int):
                    raise ValueError("page must be an integer")
                if page < 1:
                    raise ValueError("page must be greater than 0")

            # validate sort
            if sort is not None:
                if not isinstance(sort, dict):
                    raise ValueError("sort must be a dict")
                for key, value in sort.items():
                    if not isinstance(key, str):
                        raise ValueError("sort key must be a string")
                    if not isinstance(value, Sort):
                        raise ValueError("sort value must be an instance of Sort")

                # translate keys in sort
                new_sort = {}
                for key, value in sort.items():
                    if key in key_map:
                        new_key = key_map[key]
                        new_sort[new_key] = value
                    else:
                        raise ValueError(f"Key '{key}' is not allowed. Allowed keys are: {', '.join(key_map.keys())}")
                sort = new_sort

            # create args
            kwargs = bound_arguments.arguments
            kwargs["search"] = search
            if limit is not None:
                kwargs["limit"] = limit
            if page is not None:
                kwargs["page"] = page
            if sort is not None:
                kwargs["sort"] = sort

            return func(**kwargs)

        return wrapper

    return decorator
