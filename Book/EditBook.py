from typing import Dict

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from Book.BookModels import BookManipulation
from DataModels import Status
from GlobalSession import GlobalSession
from models import Book

router = APIRouter()



@router.put("/books/{id_}")
def book_update(id_: int, book: BookManipulation) -> Status:
  with Session(GlobalSession.engine) as session:
    db_book = session.query(Book).filter(Book.id == id_).first()
    if db_book is None:
      raise HTTPException(status_code=404, detail="Book not found")
    for key, value in vars(book).items():
      setattr(db_book, key, value)
    session.commit()
  return Status(status='ok')

