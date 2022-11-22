# pylint: disable=redefined-outer-name, unused-argument

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from respx import MockRouter

from tl_challenge.app import get_basic_information
from tl_challenge.models import BasicInfo


@pytest.mark.asyncio
async def test_get_basic_information(
    mock_pokeapi: MockRouter,
) -> None:
    """Tests that basic information retrieval from pokeapi works, mocking
    pokeapi service."""
    async with AsyncClient() as client:
        res = await get_basic_information(client, "mewtwo")
    assert isinstance(res, BasicInfo)
    assert res.name == "mewtwo"
    assert res.habitat == "rare"
    assert res.is_legendary is True


def test_basic_endpoint(client: TestClient, mock_pokeapi: MockRouter) -> None:
    """Tests basic endpoint behaviour."""
    res = client.get("/pokemon/mewtwo")
    # mock.assert_called_once()
    assert res.status_code == 200
    assert res.json()["name"] == "mewtwo"
    assert res.json()["habitat"] == "rare"
    assert res.json()["isLegendary"] is True


def test_basic_endpoint_error(client: TestClient, mock_pokeapi: MockRouter) -> None:
    """Tests basic endpoint behaviour."""
    res = client.get("/pokemon/asdasd")
    assert res.status_code == 404
    assert res.json() == {
        "detail": "Not Found",
    }
