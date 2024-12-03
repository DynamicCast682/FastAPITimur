from typing import Type, Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from GlobalSession import GlobalSession
from models import Category

router = APIRouter()


class CategoryResponse(BaseModel):
  id: int
  name: str

@router.get("/categories")
def get_categories() -> list[CategoryResponse]:
  with Session(GlobalSession.engine) as session:
    return session.query(Category).all()


@router.get("/categories/{id_}")
def get_category_by_id(id_: int) -> CategoryResponse:
  with Session(GlobalSession.engine) as session:
    category = session.query(Category).filter(Category.id == id_).first()
    if category is None:
      raise HTTPException(status_code=404, detail="Category not found")
    return category
