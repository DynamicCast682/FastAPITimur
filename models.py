# 1.	Модели данных (Pydantic Models и SQLAlchemy):
# •	Книга:
# Поля:
# •	Название (обязательно)
# •	Автор (обязательно)
# •	Категория (ForeignKey на категорию)
# •	Дата добавления (auto_now_add)
# •	Дата последнего обновления (auto_now)
# •	Категория:
# Поля:
# •	Название категории (уникальное, обязательно)
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime


class Base(DeclarativeBase):
  ...

class Book(Base):
  __tablename__ = 'books'
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, index=True)
  author = Column(String, index=True)
  category_id = Column(Integer, ForeignKey("categories.id"))
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Category(Base):
  __tablename__ = 'categories'
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, unique=True, index=True)