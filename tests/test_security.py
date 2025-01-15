from http import HTTPStatus

from jwt import decode

from fastpy_todo.security import create_access_token, settings


def test_jwt():
    data = {'sub': 'test@example.com'}
    token = create_access_token(data)

    decoded = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded['sub'] == data['sub']
    assert decoded['exp']  # Tests if the exp exp value was added to the token


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer invalid-token'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
