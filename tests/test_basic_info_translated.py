# pylint: disable=redefined-outer-name


from fastapi.testclient import TestClient
from respx import MockRouter


def test_basic_endpoint_translated(
    client: TestClient, mock_pokeapi: MockRouter, mock_funtranslation_api: MockRouter
) -> None:
    """Tests basic endpoint behaviour."""
    # use diglett because its habitat is cave and triggers yoda translation
    # that is mocked to give 200
    res = client.get("/pokemon/translated/diglett")
    assert res.status_code == 200
    assert res.json() == {
        "name": "diglett",
        "description": "translated text",
        "habitat": "cave",
        "isLegendary": False,
        "translated": True,
    }


def test_basic_endpoint_translated_rate_limited(
    client: TestClient, mock_pokeapi: MockRouter, mock_funtranslation_api: MockRouter
) -> None:
    """Tests basic endpoint behaviour when rate limit is triggered."""
    # use mewtwo because its habitat is not cave and triggers shakespeare translation
    # that is mocked to give 429
    res = client.get("/pokemon/translated/mewtwo")
    assert res.status_code == 200
    assert res.json()["name"] == "mewtwo"
    assert res.json()["habitat"] == "rare"
    assert res.json()["isLegendary"] is True
    assert res.json()["translated"] is False
    assert res.json()["description"] != "translated text"
