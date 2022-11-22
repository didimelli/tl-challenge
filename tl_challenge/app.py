"""This file contains the endpoints.

1. GET /pokemon/<pokemon_name>
2. GET /pokemon/translated/<pokemon_name>
"""

from fastapi import FastAPI
from fastapi import HTTPException
from httpx import AsyncClient
from httpx import HTTPStatusError

from tl_challenge.models import BasicInfo
from tl_challenge.models import BasicInfoTranslated

app = FastAPI()
POKE_API = "https://pokeapi.co/api/v2"
FUNTRANSLATION_API = "https://api.funtranslations.com/translate"


async def get_basic_information(client: AsyncClient, name: str) -> BasicInfo | None:
    """Abstracts the pokeapi call."""
    res = await client.get(POKE_API + f"/pokemon-species/{name}")
    if res.is_success:
        return BasicInfo.from_pokeapi_response(res.json())
    res.raise_for_status()
    return None


async def get_translated_description(
    client: AsyncClient, description: str, api_path: str
) -> str | None:
    """Translate a description via the funtranslation api."""
    res = await client.post(
        FUNTRANSLATION_API + "/" + api_path, json={"text": description}
    )
    # ! check status code for rate limit!
    if res.status_code == 429:
        raise HTTPStatusError("rate limiting hit", request=res.request, response=res)
    if res.is_success:
        return res.json()["contents"]["translated"]
    res.raise_for_status()
    return None


@app.get("/pokemon/{pokemon_name}")
async def get_basic_pokemon_information(pokemon_name: str):
    """Given `pokemon_name`, returns standard description and some additional
    information."""
    async with AsyncClient() as client:
        try:
            info = await get_basic_information(client, pokemon_name)
            if info is None:
                raise HTTPException(status_code=500, detail="No response from pokeapi.")
            return info
        except HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code) from e


@app.get("/pokemon/translated/{pokemon_name}")
async def get_basic_pokemon_information_translated(
    pokemon_name: str,
) -> BasicInfoTranslated:
    """Same as the other endpoint, but this time apply some transformation."""
    async with AsyncClient() as client:
        try:
            info = await get_basic_information(client, pokemon_name)
            if info is None:
                raise HTTPException(status_code=500, detail="No response from pokeapi.")
            translated = False
            try:
                if info.habitat == "cave":
                    new_description = await get_translated_description(
                        client, info.description, "yoda.json"
                    )
                    translated = True
                else:
                    new_description = await get_translated_description(
                        client, info.description, "shakespeare.json"
                    )
                    translated = True
            except HTTPStatusError:
                new_description = info.description
            if new_description is None:
                new_description = info.description
            info.description = new_description
            return BasicInfoTranslated.from_basic_info(info, translated)
        except HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code) from e
