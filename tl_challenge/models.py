"""Here the models are defined."""
import random
import string
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
        description = random.choice(english_descriptions)
        return cls(
            name=res["name"],
            description="".join(
                ch if ch not in string.whitespace else " " for ch in description
            ),
            habitat=res["habitat"]["name"],
            is_legendary=res["is_legendary"],
        )


class BasicInfoTranslated(BasicInfo):
    """Same as basic info but contains information about whether the info has
    been translated."""

    translated: bool

    @classmethod
    def from_basic_info(
        cls, info: BasicInfo, translated: bool
    ) -> "BasicInfoTranslated":
        """Builds the object from the basic info object."""
        return cls(**info.dict(), translated=translated)
