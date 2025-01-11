from dataclasses import asdict

from sqlalchemy import select

from fastpy_todo.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='testusername',
            email='test@test.com',
            password='my_password',
        )
        session.add(new_user)
        session.commit()

        user = session.scalar(
            select(User).where(User.username == 'testusername')
        )

        assert asdict(user) == {
            'id': 1,
            'username': 'testusername',
            'password': 'my_password',
            'email': 'test@test.com',
            'created_at': time,
            'updated_at': time,
        }
