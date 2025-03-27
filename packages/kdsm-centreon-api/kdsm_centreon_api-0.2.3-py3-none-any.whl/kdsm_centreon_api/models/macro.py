from typing import Any, Optional

from kdsm_centreon_api.models.base import Model
from pydantic.fields import Field


class Macro(Model):
    name: str = Field(default=..., description="Name of the macro.")
    value: str = Field(default=..., description="Value of the macro.")
    is_password: bool = Field(default=False, description="Is the macro a password.")
    description: Optional[str] = Field(default="", description="Description of the macro.")

    def __init__(self, **data: Any):
        description = data.get("description", None)
        if description is None:
            data["description"] = ""
        super().__init__(**data)
