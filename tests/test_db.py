from sqlalchemy import select

from fastpy_todo.models import User


def test_create_user(session):
    user = User(
        username='testusername',
        email='test@test.com',
        password='my_password',
    )

    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == 'test@test.com'))

    assert result.id == 1
