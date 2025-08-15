import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi.testclient import TestClient
from fastapi import status
from main import app

client = TestClient(app)

def test1():
  """
  Checks the health-check route is returning as expected
  """

  resp = client.get('/health-check')
  assert resp.status_code == status.HTTP_200_OK
  assert resp.json() == { "status": "ok"}