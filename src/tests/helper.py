from typing import List
import re

from fastapi.testclient import TestClient
from fastapi.routing import APIRoute

from app.main import app

def _get_token(username: str, password: str, client: TestClient):
    return client.post(
        "/api/v1/login",
        data={
            "username": username,
            "password": password
        },
        headers={"content-type": "application/x-www-form-urlencoded"}
    )
