from http import HTTPStatus

from fastapi import FastAPI

from fastpy_todo.routers import auth, users
from fastpy_todo.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'hello world'}
