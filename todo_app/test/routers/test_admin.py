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
from routers.admin import get_current_user, get_db
from test.utils import TestingSessionLocal, override_get_db, override_get_current_user, engine
from test_todos import test_todo


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


def test1(test_todo):
  """
  Gets all the todos when the authenticated user is an admin
  """
  resp = client.get('/admin/todos')

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
  Deletes a specified todo when using a admin user
  """

  db = TestingSessionLocal()
  todo = db.query(Todos).first()

  resp = client.delete(f'/admin/todos/{todo.id}')

  assert resp.status_code == status.HTTP_204_NO_CONTENT

  db = TestingSessionLocal()
  todo2 = db.query(Todos).filter(Todos.id == todo.id).first()

  assert todo2 is None