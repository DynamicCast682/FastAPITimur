from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base



class GlobalSession:
  engine = create_engine('sqlite:///sqll.db')
  Base.metadata.drop_all(engine)
  Base.metadata.create_all(engine)
  Session = sessionmaker(bind=engine)
  session = Session()