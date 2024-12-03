from typing import Type, Dict

from alembic.util import status
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from DataModels import Status
from GlobalSession import GlobalSession
from models import Category

router = APIRouter()


@router.delete("/categories/{id_}")
def delete_category(id_: int) -> Status:
  with Session(GlobalSession.engine) as session:
    category = session.query(Category).filter(Category.id == id_).first()
    if not category:
      raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
  return {
    "status": "ok"
  }