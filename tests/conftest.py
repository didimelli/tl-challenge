# pylint: disable=redefined-outer-name

import json
from typing import Any
from typing import Generator

from fastapi.testclient import TestClient
from httpx import Response
from pytest import fixture
from respx import MockRouter

from tl_challenge.app import FUNTRANSLATION_API
from tl_challenge.app import POKE_API
from tl_challenge.app import app


@fixture
def client() -> Generator[TestClient, None, None]:
    """Yields a testing client."""
    yield TestClient(app)


@fixture
def mewtwo() -> Generator[dict[str, Any], None, None]:
    """Yields the pokeapi response for mewtwo entry."""
    with open("tests/files/mewtwo.json", encoding="utf-8") as f:
        yield json.loads(f.read())


@fixture
def diglett() -> Generator[dict[str, Any], None, None]:
    """Yields the pokeapi response for diglett entry (useful because
    habitat==cave)."""
    with open("tests/files/diglett.json", encoding="utf-8") as f:
        yield json.loads(f.read())


@fixture
def yoda() -> Generator[dict[str, Any], Any, Any]:
    """Yields a funtranslation api response."""
    yield {
        "success": {"total": 1},
        "contents": {
            "translation": "yoda",
            "text": "Master Obiwan has lost a planet.",
            "translated": "translated text",
        },
    }


@fixture
def mock_pokeapi(
    mewtwo: dict[str, Any], diglett: dict[str, Any]
) -> Generator[MockRouter, None, None]:
    """Mocks pokeapi."""
    with MockRouter(base_url=POKE_API, assert_all_called=False) as mock:
        mewtwo_route = mock.get("/pokemon-species/mewtwo")
        mewtwo_route.return_value = Response(200, json=mewtwo)
        diglett_route = mock.get("/pokemon-species/diglett")
        diglett_route.return_value = Response(200, json=diglett)
        not_found_route = mock.get("/pokemon-species/asdasd")
        not_found_route.return_value = Response(404)
        yield mock


@fixture
def mock_funtranslation_api(yoda: dict[str, Any]) -> Generator[MockRouter, None, None]:
    """Mocks funtranslation api."""
    with MockRouter(base_url=FUNTRANSLATION_API, assert_all_called=False) as mock:
        yoda_route = mock.post("/yoda.json")
        yoda_route.return_value = Response(200, json=yoda)
        shakespeare_route = mock.post("/shakespeare.json")
        shakespeare_route.return_value = Response(429)  # to test rate limiting
        yield mock
