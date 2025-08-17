import os
import sys
from unittest.mock import ANY
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, text
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from models import Todos
from routers.todos import get_current_user, get_db
from test.utils import TestingSessionLocal, override_get_db, override_get_current_user, engine


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


@pytest.fixture
def test_todo():
  todo = Todos(
    title="Test todo",
    description="This is a todo for testing",
    priority=5,
    complete=False,
    owner_id=1
  )

  db = TestingSessionLocal()
  db.add(todo)
  db.commit()
  yield todo

  with engine.connect() as connection:
    connection.execute(text("DELETE FROM todos;"))
    connection.commit()


def test1(test_todo):
  """
  Gets all the todos for an authenticated user
  """

  resp = client.get('/todos')
  assert resp.status_code == status.HTTP_200_OK
  assert resp.json() == [{
    "complete": False,
    "title": "Test todo",
    "description": "This is a todo for testing",
    "priority": 5,
    "owner_id": 1,
    "id": ANY
  }]


def test2(test_todo):
  """
  Gets the specified todo for an authenticated user
  """
  db = TestingSessionLocal()
  todo = db.query(Todos).first()

  resp = client.get(f'/todos/{todo.id}')

  assert resp.status_code == status.HTTP_200_OK
  assert resp.json().get('title') == todo.title
  assert resp.json().get('description') == todo.description
  assert resp.json().get('id') == todo.id
  assert resp.json().get('priority') == todo.priority
  assert resp.json().get('owner_id') == todo.owner_id
  assert resp.json().get('complete') == todo.complete

def test3(test_todo):
  """
  Returns an error when the todo is not found for an authenticated user
  """

  resp = client.get('/todos/1')
  assert resp.status_code == status.HTTP_404_NOT_FOUND
  assert resp.json() == {
    "detail": "Todo not found"
  }


def test4(test_todo):
  """
  Creates a todo for an autheticated user
  """

  req_data = {
    "complete": False,
    "title": "Test todo2",
    "description": "This is a todo for testing2",
    "priority": 5,
    "owner_id": 1
  }

  resp = client.post('/todos', json=req_data)

  assert resp.status_code == status.HTTP_201_CREATED

  db = TestingSessionLocal()
  todo = db.query(Todos)[1]

  assert req_data.get('title') == todo.title
  assert req_data.get('description') == todo.description
  assert req_data.get('priority') == todo.priority
  assert req_data.get('owner_id') == todo.owner_id
  assert req_data.get('complete') == todo.complete


def test5(test_todo):
  """
  Updates the specified todo for an authenticated user
  """

  req_data = {
    "complete": False,
    "title": "Test todo2",
    "description": "This is a todo for testing2",
    "priority": 4,
    "owner_id": 1
  }

  db = TestingSessionLocal()
  todo = db.query(Todos).first()

  resp = client.put(f'/todos/{todo.id}', json=req_data)

  assert resp.status_code == status.HTTP_204_NO_CONTENT

  db.refresh(todo)

  assert req_data.get('title') == todo.title
  assert req_data.get('description') == todo.description
  assert req_data.get('priority') == todo.priority
  assert req_data.get('owner_id') == todo.owner_id
  assert req_data.get('complete') == todo.complete


def test6(test_todo):
  """
  Returns an error when the todo is not found for an authenticated user
  """

  req_data = {
    "complete": False,
    "title": "Test todo2",
    "description": "This is a todo for testing2",
    "priority": 4,
    "owner_id": 1
  }

  resp = client.put('/todos/999999', json=req_data)

  assert resp.status_code == status.HTTP_404_NOT_FOUND
  assert resp.json() == {
    "detail": "Todo not found"
  }


def test7(test_todo):
  """
  Deletes the specified todo for an authenticated user
  """

  db = TestingSessionLocal()
  todo = db.query(Todos).first()

  resp = client.delete(f'/todos/{todo.id}')

  assert resp.status_code == status.HTTP_204_NO_CONTENT

  db = TestingSessionLocal()
  todo2 = db.query(Todos).filter(Todos.id == todo.id).first()

  assert todo2 is None
