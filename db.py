# db.py
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from flask_login import UserMixin

load_dotenv(".env.local")
DATABASE_URL = os.getenv("DATABASE_URL") 

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()




class User(Base,UserMixin):
    __tablename__ = "userdata"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    
class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    voter_id = Column(String, unique=True, index=True)
    candidate = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)



