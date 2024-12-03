from fastapi import FastAPI, APIRouter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base



class GlobalSession:
  engine = create_engine('sqlite:///sqll.db')
  app = FastAPI()
  Session = sessionmaker(bind=engine)
  session = Session()