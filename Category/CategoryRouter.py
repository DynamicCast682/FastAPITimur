from fastapi import APIRouter

from Category.GetCategory import router as get_router
from Category.AddCategory import router as add_router
from Category.DeleteCategory import router as delete_router

category_router = APIRouter()

category_router.include_router(get_router)
category_router.include_router(add_router)
category_router.include_router(delete_router)