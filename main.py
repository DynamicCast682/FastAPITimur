import uvicorn
from fastapi import FastAPI
from sqlalchemy.orm import Session

from Book.BookRouter import book_router
from Category.CategoryRouter import category_router
from GlobalSession import GlobalSession
from models import Book
from utils import ORM_random_fill

# Base.metadata.drop_all(bind=GlobalSession.engine)
# Base.metadata.create_all(bind=GlobalSession.engine)
#
# Base.metadata.clear()
with Session(GlobalSession.engine) as session:
  if not session.query(Book).first():
    ORM_random_fill()

app = FastAPI()
app.openapi_version = "3.0.3"

app.include_router(book_router, prefix="/api")
app.include_router(category_router, prefix="/api")



if __name__ == '__main__':
  uvicorn.run(app, host='127.0.0.1', port=8000)
