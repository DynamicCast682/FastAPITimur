from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from Category.CategoryModels import PydanticCategory
from DataModels import Status
from GlobalSession import GlobalSession
from models import Category

router = APIRouter()


@router.post("/categories")
def add_category(category: PydanticCategory) -> Status:
  with Session(GlobalSession.engine) as session:
    try:
      existing_category = session.query(Category).filter(Category.name == category.name).first()
      if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")
      new_category = Category(**category.model_dump())
      session.add(new_category)
      session.commit()
    except Exception as e:
      session.rollback()
      raise HTTPException(status_code=400, detail=str(e))
  return {
    "status": "ok"
  }
