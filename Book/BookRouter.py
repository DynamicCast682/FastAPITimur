from fastapi import APIRouter

from Book.GetBooks import router as get_router
from Book.AddBook import router as add_router
from Book.DeleteBook import router as delete_router
from Book.EditBook import router as update_router

book_router = APIRouter()

book_router.include_router(get_router)
book_router.include_router(add_router)
book_router.include_router(delete_router)
book_router.include_router(update_router)