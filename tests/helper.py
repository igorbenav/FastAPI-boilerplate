from fastapi.testclient import TestClient


def _get_token(username: str, password: str, client: TestClient):
    return client.post(
        "/api/v1/login",
        data={"username": username, "password": password},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
