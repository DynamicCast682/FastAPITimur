from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from Book.BookModels import BooksQuery, PyDanticBook
from GlobalSession import GlobalSession
from models import Book, Category

router = APIRouter()



@router.get("/books")
def get_books(content: BooksQuery = Depends()) -> list[PyDanticBook]:
  with Session(GlobalSession.engine) as session:
    query = session.query(
      *[getattr(Book, column.name) for column in Book.__table__.columns],
      Category.name.label('category'),
    ).join(Category)

    if content.title != '':
      query = query.filter(Book.title.ilike(f"%{content.title}%"))
    if content.author != '':
      query = query.filter(Book.author.ilike(f"%{content.author}%"))
    if content.created_at != '':
      query = query.filter(Book.created_at.ilike(f"%{content.created_at}%"))
    if content.updated_at != '':
      query = query.filter(Book.updated_at.ilike(f"%{content.updated_at}%"))


    if content.sorted_by:
      if content.sorted_by == 'category':
        order_by_column = getattr(Category, 'name')
      else:
        order_by_column = getattr(Book, content.sorted_by)
      if content.order:
        if content.order == 'asc':
          query = query.order_by(order_by_column)
        elif content.order == 'desc':
          query = query.order_by(desc(order_by_column))
        else:
          raise HTTPException(status_code=400, detail="Invalid order parameter")
      else:
        query = query.order_by(order_by_column)

    if content.offset:
      query = query.offset(content.offset)
    if content.limit:
      query = query.limit(content.limit)

    results = query.all()
    return results

@router.get("/books/{id_}")
def get_book_by_id(id_: int) -> PyDanticBook:
  with Session(GlobalSession.engine) as session:
    book = session.query(Book).filter(Book.id == id_).first()
    if book is None:
      raise HTTPException(status_code=404, detail="Book not found")
    return book