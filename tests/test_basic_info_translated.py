# pylint: disable=redefined-outer-name

from typing import Generator

from fastapi.testclient import TestClient
from pytest import fixture

from tl_challenge.app import app


@fixture
def client() -> Generator[TestClient, None, None]:
    """Yields a testing client."""
    yield TestClient(app)


def test_basic_endpoint(client: TestClient) -> None:
    """Tests basic endpoint behaviour."""
    res = client.get("/pokemon/translated/mew")
    assert res.status_code == 200
    assert res.json() == {
        "name": "mew",
        "description": "So rare yond 't is still did doth sayeth to beest "
        "a mirage by many experts. Only a few people hath't seen 't worldwide.",
        "habitat": "rare",
        "isLegendary": False,
    }
