from typing import Dict

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture()
def cliente() -> TestClient:
    return TestClient(app=app)


@pytest.fixture()
def set_json() -> Dict[str, str]:
    return {"key": "string", "value": "112", "sdsds": "sdsds"}


def test_hello(cliente: TestClient) -> None:
    response = cliente.get("/hello")

    assert response.status_code == status.HTTP_200_OK
    assert response.content.decode() == "HSE One Love!"


def test_getset(cliente: TestClient, set_json: Dict[str, str]) -> None:
    response_set = cliente.post("/set", json=set_json)
    response_get = cliente.get("/get/string")
    response_get_404 = cliente.get("/get/string1")

    assert response_set.status_code == status.HTTP_200_OK
    assert response_get.json() == {"key": "string", "value": "112"}
    assert response_get_404.status_code == status.HTTP_404_NOT_FOUND


def test_divide(cliente: TestClient) -> None:
    response = cliente.post("/divide", json={"dividend": 5, "divider": 1})
    response_400 = cliente.post("/divide", json={"dividend": 5, "divider": 0})

    assert response.status_code == status.HTTP_200_OK
    assert response.content.decode() == "5.0"
    assert response_400.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize("url_to_test", ["/f", "/gf/h/f", "/hello/sd/fsd/sdf"])
def test_random_routes(cliente: TestClient, url_to_test: str) -> None:
    response = cliente.get(url_to_test)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
