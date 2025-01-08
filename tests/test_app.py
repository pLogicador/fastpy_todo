from http import HTTPStatus

from fastapi.testclient import TestClient

from fastpy_todo.app import app


def test_read_root_should_return_ok_and_hello_world():
    client = TestClient(app)  # Arrange
    response = client.get('/')  # Act
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'hello world'}
