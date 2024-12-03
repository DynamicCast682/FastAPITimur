from typing import Dict

from fastapi import APIRouter
from fastapi import HTTPException
from sqlalchemy.orm import Session

from Book.BookModels import BookManipulation
from DataModels import Status
from GlobalSession import GlobalSession
from models import Book

router = APIRouter()


@router.post("/books")
def add_book(book: BookManipulation) -> Status:
  with Session(GlobalSession.engine) as session:
    try:
      book = Book(**book.model_dump())
      session.add(book)
      session.commit()
    except Exception as e:
      session.rollback()
      raise HTTPException(status_code=400, detail=str(e))
  return Status(status='ok')
