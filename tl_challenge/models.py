"""Here the models are defined."""
from typing import Any

from pydantic import BaseModel
from pydantic import Field


class BasicInfo(BaseModel):
    """Represents pokemon basic info."""

    name: str
    description: str
    habitat: str
    is_legendary: bool = Field(..., alias="isLegendary")

    class Config:
        """Internal config for pydantic aliases."""

        allow_population_by_field_name = True

    @classmethod
    def from_pokeapi_response(cls, res: dict[str, Any]) -> "BasicInfo":
        """Builds the object directly from the pokeapi response body."""
        return cls(
            name=res["name"],
            description=res["flavor_text_entries"][0]["flavor_text"],
            habitat=res["habitat"]["name"],
            is_legendary=res["is_legendary"],
        )
