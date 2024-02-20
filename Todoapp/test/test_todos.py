from sqlalchemy import StaticPool, create_engine, text
from ..database import Base
from sqlalchemy.orm import sessionmaker
from ..main import app
from ..routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from ..models import Todos

SQLALCHEMY_DATEBASE_URL = "sqlite:///./testdb.db"

"""Connect to databse for simulation test"""
engine = create_engine(
    SQLALCHEMY_DATEBASE_URL,
    connect_args={"check_same_thread": False},
    poolclass= StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_cuurent_user():
    return {'username': 'jefe',  'id': 1, 'user_role':'admin'}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_cuurent_user



@pytest.fixture
def test_todo():
    todo = Todos(
        title='Learn to code!',
        description='Need to learn everyday',
        priority=5,
        complete=False,
        owner = 1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

client = TestClient(app)

def test_read_all_authenticated(test_todo):
    """test for read all todo with user is athenticated"""
    response = client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': 'Learn to code!',
                                'description': 'Need to learn everyday', 'id':1,
                                'priority': 5, 'owner':1}]

def test_read_one_authenticated(test_todo):
    response = client.get("/todos/Todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete': False, 'title': 'Learn to code!',
                                'description': 'Need to learn everyday', 'id':1,
                                'priority': 5, 'owner':1}

def read_one_authenticated_not_found():
    response = client.get("/todos/Todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail':'Todo not found'}

def test_create_todo(test_todo):
    request_data ={
        'title': 'New todo',
        'description': 'New todo description',
        'priority': 5,
        'complete': False,
    }

    response = client.post('/todos/create', json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

def test_update_todo(test_todo):
    request_data ={
        'title': 'Update todo',
        'description': 'New todo description',
        'priority': 5,
        'complete': False,
    }
    response = client.put("/todos/update/1", json=request_data)
    assert response.status_code ==204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id ==1).first()
    assert model.title == 'Update todo'

def test_update_todo_not_found(test_todo):
    request_data ={
        'title': 'Update todo',
        'description': 'New todo description',
        'priority': 5,
        'complete': False,
    }
    response = client.put("/todos/update/999", json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": 'Todo not found'}

def test_delete_todo(test_todo):
    response = client.delete("todos/delete/1")
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found():
    response = client.delete("todos/delete/999")
    assert response.status_code == 404
    assert response.json() == {"detail": 'Todo not found'}