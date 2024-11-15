import datetime
from typing import Optional

import pandas as pd
import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from unicodedata import category

from GlobalSession import GlobalSession
from models import Base, Book, Category
from utils import ORM_random_fill

app = FastAPI()




ORM_random_fill()


class Data(BaseModel):
  user: Optional[str] = None

@app.get("/api/")
def main(data: Data = Depends()):
  return data

@app.post("/api/")
def main(data: Data = Depends()):
  return data

class BooksQuery(BaseModel):
  limit: Optional[int] = None
  offset: Optional[int] = None
  sorted_by: Optional[str] = None
  order: Optional[str] = None
  title: Optional[str] = None
  author: Optional[str] = None
  created_at: Optional[str] = None
  updated_at: Optional[str] = None


@app.get("/api/books/")
def get_books(content: BooksQuery = Depends()):
  with Session(GlobalSession.engine) as session:
    mass = []
    for model in session.query(Book).all():
      category_name = session.query(Category).filter(Category.id == model.category_id).first().name
      mass.append(
        {
          'id': model.id,
          'title': model.title,
          'author': model.author,
          'category_id': model.category_id,
          'category_name': category_name,
          'created_at': model.created_at,
          'updated_at': model.updated_at
        }
      )
    frame = pd.DataFrame(mass, columns=['id', 'title', 'author', 'category_id', 'category_name', 'created_at', 'updated_at'])


    if content.title:
      frame = frame[frame['title'] == content.title]
    if content.author:
      frame = frame[frame['author'] == content.author]
    if content.created_at:
      frame = frame[frame['created_at'] == content.created_at]
    if content.updated_at:
      frame = frame[frame['updated_at'] == content.updated_at]

    if content.sorted_by:
      if content.sorted_by == 'category':
        content.sorted_by = 'category_name'
      frame = frame.sort_values(by=content.sorted_by)
      ascending = True
      if content.order == 'desc':
        ascending = False
      elif content.order == 'asc':
        ascending = True
      frame = frame.sort_values(by=content.sorted_by, ascending=ascending)
    start = 0
    if content.offset:
      start = content.offset
    end = 10
    if content.limit:
      end = content.limit + start

    frame = frame[start:end]



    return frame.to_dict(orient='records')

class AddBook(BaseModel):
  title: str
  author: str
  category_id: int


@app.post("/api/books/")
def add_book(book: AddBook):
  with Session(GlobalSession.engine) as session:
    book = Book(**book.model_dump())
    session.add(book)
    session.commit()

@app.get("/api/books/{id}")
def get_book_by_id(id: int):
  with Session(GlobalSession.engine) as session:
    return session.query(Book).filter(Book.id == id).first()


class EditBook(BaseModel):
  title: str
  author: str
  category_id: int

@app.put("/api/books/{id}")
def book_update(book: EditBook, id: int):
  with Session(GlobalSession.engine) as session:
    db_book = session.query(Book).filter(Book.id == id).first()
    print(book.model_dump())
    db_book.title = book.title
    db_book.author = book.author
    db_book.category_id = book.category_id
    session.commit()

@app.delete("/api/books/{id}")
def book_delete(id: int):
  with Session(GlobalSession.engine) as session:
    book = session.query(Book).filter(Book.id == id).first()
    session.delete(book)
    session.commit()




@app.get("/api/categories/")
def get_categories():
  with Session(GlobalSession.engine) as session:
    sl = {}
    for model in session.query(Category).all():
      sl.update(
        {
          model.id: model.name
        }
      )
    return sl

class AddCategory(BaseModel):
  name: str

@app.post("/api/categories/")
def add_category(category: AddCategory):
  with Session(GlobalSession.engine) as session:
    category = Category(name=category.name)
    session.add(category)
    session.commit()

@app.get("/api/categories/{id}")
def get_category_by_id(id: int):
  with Session(GlobalSession.engine) as session:
    return session.query(Category).filter(Category.id == id).first()

if __name__ == '__main__':
  uvicorn.run(app, host='127.0.0.1', port=8000)


