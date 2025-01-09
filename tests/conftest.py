import pytest
from fastapi.testclient import TestClient

from fastpy_todo.app import app


@pytest.fixture
def client():
    return TestClient(app)
