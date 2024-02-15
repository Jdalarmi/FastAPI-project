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
    response = client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': 'Learn to code!',
                                'description': 'Need to learn everyday', 'id':1,
                                'priority': 5, 'owner':1}]