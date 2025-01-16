from http import HTTPStatus

from fastpy_todo.schemas import UserPublic
from fastpy_todo.security import create_access_token


def test_create_user(client):
    response = client.post(  # UserSchema
        '/users/',
        json={
            'username': 'testusername',
            'email': 'test@test.com',
            'password': 'password',
        },
    )

    # Validate the status code
    assert response.status_code == HTTPStatus.CREATED

    # Validate UserPublic
    assert response.json() == {
        'username': 'testusername',
        'email': 'test@test.com',
        'id': 1,
    }


def test_create_user_should_return_400_username_exists(client, user, token):
    response = client.post(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': user.username,
            'email': 'test@test.com',
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_create_user_should_return_400_email_exists(client, user, token):
    response = client.post(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'testusername',
            'email': user.email,
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'newtestusername',
            'email': 'newtest@test.com',
            'password': 'newpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'newtestusername',
        'email': 'newtest@test.com',
        'id': user.id,
    }


def test_update_integrity_error(client, user, token):
    # Inserting fictitious user
    client.post(
        '/users',
        json={
            'username': 'testusername',
            'email': 'test@example.com',
            'password': 'testpassword',
        },
    )

    # Changing the user of the fixture for fictitious user
    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'testusername',
            'email': 'newtest@example.com',
            'password': 'newtestpassword',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or Email already exists'
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User has been deleted!!'}


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'testusername',
            'email': 'test@test.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user_with_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_get_user_by_id_should_return_not_found(client):
    response = client.get('/users/5')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'This user is not found'}


def test_get_user_by_id(client, user, token):
    response = client.get(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_get_current_user_not_found(client):
    data = {'no-email': 'test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_does_not_exists(client):
    data = {'sub': 'test@example.com'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
