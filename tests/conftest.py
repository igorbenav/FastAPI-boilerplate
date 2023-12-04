import pytest
from fastapi.testclient import TestClient

from src.app.main import app

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as _client:
        yield _client
