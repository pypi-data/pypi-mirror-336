from enum import Enum


class CentreonVersion(str, Enum):
    v24_04 = "v24.04"
    v23_10 = "v23.10"
    v23_04 = "v23.04"
    v22_10 = "v22.10"
    v22_04 = "v22.04"
    LATEST = "v24.04"  # must be last Enum value
