import os
import sys
from unittest.mock import ANY
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import status
from fastapi.testclient import TestClient
from main import app
from models import Users
from routers.users import get_current_user, get_db
from test.utils import TestingSessionLocal, override_get_db, override_get_current_user


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


def test1():
  """
  Returns the current user
  """

  resp = client.get('/users/me')

  assert resp.status_code == status.HTTP_200_OK

  db = TestingSessionLocal()
  user = db.query(Users).first()

  assert resp.json().get('id') == user.id
  assert resp.json().get('email') == user.email
  assert resp.json().get('first_name') == user.first_name
  assert resp.json().get('last_name') == user.last_name
  assert resp.json().get('username') == user.username