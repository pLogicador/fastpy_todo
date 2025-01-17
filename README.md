# FastPy To-do

Este é um projeto de uma API para gerenciamento de tarefas. A aplicação permite operações CRUD (Criar, Ler, Atualizar, Deletar) em tarefas, com autenticação de usuários utilizando JWT.

## Funcionalidades

- **Autenticação de Usuários**: Registro e login de usuários com tokens JWT para autenticação segura.
- **Gerenciamento de Tarefas**: Criação, visualização, atualização e exclusão de tarefas associadas a usuários autenticados.

## Dependências

### `fastapi`: Framework para construção de APIs.
### `sqlalchemy`: ORM para manipulação do banco de dados.
### `pydantic-settings`: Para configuração baseada em Pydantic.
### `alembic`: Para migração de banco de dados.
### `pwdlib[argon2]`: Para hash de senhas.
### `python-multipart`: Para manipulação de arquivos em formulários.
### `pyjwt`: Para gerar e verificar JWTs (tokens de autenticação).
### `tzdata`: Para dados de fusos horários.

</br>

## Estrutura do Projeto

A estrutura do projeto está organizada da seguinte forma:

```bash
fastpy_todo/
├── fastpy_todo/
│   ├── __init__.py
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   └── settings.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── todo.py
│   │   └── users.py    
├── migrations/
│   ├── versions/
│   ├── README
│   ├── env.py
│   └── script.py.mako
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_app.py
│   ├── test_auth.py
│   ├── test_db.py
│   ├── test_security.py
│   ├── test_todo.py
│   └── test_users.py
├── .gitignore
├── README.md
├── alembic.ini
├── poetry.lock
└── pyproject.toml
```

</br>

## Como Executar o Projeto

### 1. Clone o repositório:

```bash
git clone https://github.com/pLogicador/fastpy_todo.git
cd fastpy_todo
```
### 2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```
### 3. Instale as dependências:

```bash
pip install -r requirements.txt
```
### 4. Configure as variáveis de ambiente:

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
### 5. Execute as migrações do banco de dados:

```bash
alembic upgrade head
```
### 6. Inicie a aplicação:

```bash
uvicorn fastpy_todo.main:app --reload
```
### 7. Acesse a documentação interativa:

Abra o navegador e vá para `http://127.0.0.1:8000/docs` para acessar a interface do Swagger UI.

Testes
Para executar os testes, utilize o `pytest`:

```bash
pytest
```
</br>

## Créditos
Este projeto foi desenvolvido com base no curso [FastAPI do Zero](https://fastapidozero.dunossauro.com/), ministrado por [Dunossauro](https://github.com/dunossauro).
