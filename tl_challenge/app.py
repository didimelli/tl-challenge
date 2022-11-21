"""This file contains the endpoints.

1. GET /pokemon/<pokemon_name>
2. GET /pokemon/translated/<pokemon_name>
"""


from fastapi import FastAPI
from httpx import AsyncClient

from tl_challenge.models import BasicInfo

app = FastAPI()
POKE_API = "https://pokeapi.co/api/v2"


@app.get("/pokemon/{pokemon_name}")
async def get_basic_pokemon_information(pokemon_name: str):
    """Given `pokemon_name`, returns standard description and some additional
    information."""
    async with AsyncClient() as client:
        res = await client.get(POKE_API + f"/pokemon-species/{pokemon_name}")
    return BasicInfo.from_pokeapi_response(res.json())
