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
    res = client.get("/pokemon/mewtwo")
    assert res.status_code == 200
    assert res.json() == {
        "name": "mewtwo",
        "description": "It was created by\na scientist after\nyears of horrific\x0c"
        "gene splicing and\nDNA engineering\nexperiments.",
        "habitat": "rare",
        "isLegendary": True,
    }
