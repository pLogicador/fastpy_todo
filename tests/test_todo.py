from http import HTTPStatus

from fastpy_todo.models import TodoState
from tests.conftest import TodoFactory


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test tile',
            'description': 'Test description',
            'state': 'draft',
        },
    )
    assert response.json() == {
        'id': 1,
        'title': 'Test tile',
        'description': 'Test description',
        'state': 'draft',
    }


def test_list_todos_should_return_five_todos(session, client, user, token):
    expected_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/',  # not query
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_pagination_should_return_two_todos(
    session, client, user, token
):
    expected_todos = 2
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_title_should_return_five_todos(
    session, client, user, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, title='Test title')
    )
    session.commit()

    response = client.get(
        '/todos/?title=Test title',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_description_should_return_five_todos(
    session, client, user, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(
            5, user_id=user.id, description='Test description'
        )
    )
    session.commit()

    response = client.get(
        '/todos/?description=desc',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_state_should_return_five_todos(
    session, client, user, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, state=TodoState.done)
    )
    session.commit()

    response = client.get(
        '/todos/?state=done',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_combined_should_return_five_todos(
    session, user, client, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            title='Test todo combined',
            description='combined description',
            state=TodoState.done,
        )
    )

    session.bulk_save_objects(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title='Other title',
            description='other description',
            state=TodoState.todo,
        )
    )
    session.commit()

    response = client.get(
        '/todos/?title=Test todo combined&description=combined&state=done',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Task has been deleted successfully!!'
    }


def test_delete_todo_error(client, token):
    response = client.delete(
        f'/todos/{10}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.patch(
        f'/todos/{todo.id}',
        json={'title': 'testtitle'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'testtitle'


def test_patch_todo_error(client, token):
    response = client.patch(
        f'/todos/{10}', json={}, headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}
