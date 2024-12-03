import datetime
from functools import lru_cache

import pandas as pd
import numpy as np
from sqlalchemy import select

from sqlalchemy.orm import Session

from GlobalSession import GlobalSession
from models import Book, Category


@lru_cache(None)
def get_random_books():
  frame = pd.read_csv('book_levels.csv')
  frame = frame.dropna().drop_duplicates()
  frame: pd.DataFrame = frame.rename(columns={
    'Title': 'title',
    'Author': 'author',
    'Language Level': 'category'
  })
  date_range = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
  date_range = date_range.to_numpy()[:frame.__len__()]
  np.random.shuffle(date_range)
  frame['created_at'] = date_range.copy()
  np.random.shuffle(date_range)
  frame['updated_at'] = date_range.copy()
  print(type(date_range[0]))
  return frame

@lru_cache(None)
def ORM_random_fill():
  books_frame = get_random_books()
  with GlobalSession.session as session:
    for i in range(books_frame.__len__()):
      book = books_frame.iloc[i]
      assert type(book) is pd.Series, f'book is not pd.Series: {book}'
      category = book['category']
      assert type(category) is str
      query = select(Category).where(Category.name == category)
      db_category = session.execute(query).scalars().first()
      if not db_category:
        db_category = Category(name=category)
        session.add(db_category)
        session.commit()
        session.refresh(db_category)  # Refresh to get the id
      created_at: pd.Timestamp = book['created_at']
      updated_at: pd.Timestamp = book['updated_at']
      session.add(Book(
        title=book['title'],
        author=book['author'],
        category_id=db_category.id,
        created_at=created_at.to_pydatetime(),
        updated_at=updated_at.to_pydatetime()
      ))
    session.commit()
  return books_frame
