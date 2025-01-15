from http import HTTPStatus


def test_read_root_should_return_ok_and_hello_world(client):
    response = client.get('/')  # Act
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'hello world'}
