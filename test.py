from fastapi.testclient import TestClient
from main import app
from utils import ORM_random_fill
import pytest
import pandas as pd

@pytest.fixture(scope="module")
def client():
  return TestClient(app)

@pytest.fixture(scope="module")
def fill_random_books():
    frame = ORM_random_fill()
    assert type(frame) is pd.DataFrame
    assert frame.__len__() > 0

def test_get_books(client):
    response = client.get("/books")
    print(response.json())
    assert response.status_code == 200
    assert response.json().__len__() > 0
