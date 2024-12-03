import datetime
from typing import Optional

from pydantic import BaseModel


class BooksQuery(BaseModel):
  limit: int
  offset: int
  sorted_by: str
  order: str
  title: str = ''
  author: str = ''
  created_at: str = ''
  updated_at: str = ''


class PyDanticBook(BaseModel):
  id: int
  title: str
  author: str
  category_id: int
  category: str
  created_at: datetime.datetime
  updated_at: datetime.datetime

class BookManipulation(BaseModel):
  title: str
  author: str
  category_id: int