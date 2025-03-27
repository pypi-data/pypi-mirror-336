from enum import Enum


class SnmpVersion(str, Enum):
    v1 = "1"
    v2 = "2c"
    v3 = "3"
