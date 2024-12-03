from alembic.util import status
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from DataModels import Status
from GlobalSession import GlobalSession
from models import Book

router = APIRouter()

@router.delete("/books/{id_}")
def book_delete(id_: int) -> Status:
  with Session(GlobalSession.engine) as session:
    book = session.query(Book).filter(Book.id == id_).first()
    if not book:
      raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
  return Status(status='ok')

