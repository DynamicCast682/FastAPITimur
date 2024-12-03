import time
import uuid

import numpy as np
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from utils import ORM_random_fill
import pytest
import pandas as pd
from GlobalSession import GlobalSession
from models import Book

pd.set_option('display.max_columns', None)


@pytest.fixture(scope="module")
def client():
  return TestClient(app)


@pytest.fixture(scope="module")
def fill_random_books():
  frame = ORM_random_fill()
  assert type(frame) is pd.DataFrame
  assert frame.__len__() > 0
  return frame


def books2pandas(sl: dict) -> pd.DataFrame:
  frame = pd.DataFrame(sl)
  del frame['id']
  del frame['category_id']
  # print(frame.columns)
  return frame.astype({
    'title': 'string',
    'author': 'string',
    'category': 'string',
    'created_at': 'datetime64[ns]',
    'updated_at': 'datetime64[ns]'
  }).reset_index(drop=True)


def test_get_books(client):
  response = client.get("/api/books")
  print(response.json())
  assert response.status_code == 200
  assert response.json().__len__() > 0


from itertools import product


@pytest.mark.parametrize(
  "sorted_by, asc_desc, limit, offset",
  list(product(
    ['title', 'author', 'created_at', 'updated_at'],
    ['asc', 'desc'],
    [10, 20, 30, 40, 50],
    [10, 20, 30, 40, 50]
  ))
)
def test_sort(client, fill_random_books,
              sorted_by: str, asc_desc: str, limit: int, offset: int):
  frame = fill_random_books.copy().astype(
    {
      'title': 'string',
      'author': 'string',
      'category': 'string',
      'created_at': 'datetime64[ns]',
      'updated_at': 'datetime64[ns]'
    }
  )
  get_string = f"/api/books?sorted_by={sorted_by}&order={asc_desc}&limit={limit}&offset={offset}"
  # print()
  # print(get_string)

  response = client.get(get_string)
  assert response.status_code == 200
  response_json = response.json()
  # print(response_json)
  assert response_json.__len__() > 0
  exist_frame = books2pandas(response_json).reset_index(drop=True)
  right_frame = frame.sort_values(by=sorted_by, ascending=asc_desc == 'asc').iloc[offset:offset + limit].reset_index(
    drop=True)
  assert exist_frame[sorted_by].dtype == right_frame[
    sorted_by].dtype, f"{exist_frame[sorted_by].dtype} != {right_frame[sorted_by].dtype}"
  assert np.all(exist_frame[sorted_by] == right_frame[sorted_by])

def test_book_append(client):
  lp = client.get("/api/books").json().__len__()
  response = client.post("/api/books", json={
    "title": "test",
    "author": "test",
    "category_id": 1
  })
  assert response.status_code == 200
  ln = client.get("/api/books").json().__len__()
  assert ln == lp + 1

  res = client.get("/api/books?sorted_by=created_at&order=desc&limit=1")
  frame = books2pandas(res.json())
  assert frame['title'][0] == "test"


class TestCategory:
  @staticmethod
  def test_add_category(client):
    for i in range(10):
      lp = client.get("/api/categories").json().__len__()

      name = uuid.uuid4().hex
      response = client.post("/api/categories", json={"name": name})
      assert response.status_code == 200
      ln = client.get("/api/categories").json().__len__()

      assert ln == lp + 1


  @staticmethod
  def test_delete_category(client):
    for i in range(1, 10):
      assert client.get(f"/api/categories/{i}").status_code == 200
      assert client.delete(f"/api/categories/{i}").status_code == 200
      assert client.get(f"/api/categories/{i}").status_code == 404


# def test_rollback():
#   try:
#     with Session(GlobalSession.engine) as session:
#       book = Book(title="test", author="test", category_id=1)
#       session.add(book)
#       session.commit()
#       raise Exception("rollback")
#   except:
#     pass
#   with Session(GlobalSession.engine) as session:
#     book = session.query(Book).filter(Book.title == "test").first()
#     assert book is None

