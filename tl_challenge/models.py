"""Here the models are defined."""
import random
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
        english_descriptions: list[str] = [
            r["flavor_text"]
            for r in res["flavor_text_entries"]
            if r["language"]["name"] == "en"
        ]
        if not english_descriptions:
            raise ValueError("No english translation found.")
        return cls(
            name=res["name"],
            description=random.choice(english_descriptions),
            habitat=res["habitat"]["name"],
            is_legendary=res["is_legendary"],
        )
