from http import HTTPStatus

from fastpy_todo.schemas import UserPublic


def test_read_root_should_return_ok_and_hello_world(client):
    response = client.get('/')  # Act
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'hello world'}


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


def test_create_user_should_return_400_username_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'test@test.com',
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_should_return_400_email_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'email': user.email,
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


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
            'password': 'newpassword',
            'username': 'newtestusername',
            'email': 'newtest@test.com',
            'id': user.id,
        },
    )
    assert response.json() == {
        'username': 'newtestusername',
        'email': 'newtest@test.com',
        'id': user.id,
    }


def test_update_user_should_return_not_found(client):
    response = client.put(
        '/users/5',
        json={
            'password': 'newpassword',
            'username': 'newtestusername',
            'email': 'newtest@test.com',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'This user is not found'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User has been deleted!!'}


def test_delete_user_should_return_not_found(client):
    response = client.delete('/users/5')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'This user is not found'}


def test_get_user_by_id_should_return_not_found(client):
    response = client.get('/users/5')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'This user is not found'}


def test_get_user_by_id(client, user):
    response = client.get('/users/{}'.format(user.id))

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert token['access_token']
