import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

engine = create_engine("sqlite:///database.db", echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
