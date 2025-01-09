from http import HTTPStatus


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


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'testusername',
                'email': 'test@test.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'password': 'newpassword',
            'username': 'newtestusername',
            'email': 'newtest@test.com',
            'id': 1,
        },
    )
    assert response.json() == {
        'username': 'newtestusername',
        'email': 'newtest@test.com',
        'id': 1,
    }


def test_update_user_should_return_not_fount(client):
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


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User has been deleted!!'}


def test_delete_user_should_return_not_found(client):
    response = client.delete('/users/5')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'This user is not found'}


def test_get_user_by_id_should_return_not_found(client):
    response = client.get('/users/55')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'This user is not found'}


def test_get_user_by_id(client):
    # Create the user
    response = client.post(
        '/users/',
        json={
            'username': 'username',
            'email': 'test@test.com',
            'password': 'password',
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    # tests the GET /users/1 endpoint

    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'username',
        'email': 'test@test.com',
        'id': 1,
    }
