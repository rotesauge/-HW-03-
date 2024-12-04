from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String,DateTime,BINARY

from fastapi import FastAPI

SQLALCHEMY_DATABASE_URL = "sqlite:///db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

class Base(DeclarativeBase): pass

class Pereval_added(Base):
    __tablename__ = "pereval_added"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_added = Column(DateTime)
    raw_data = Column(String)
    images = Column(String)

class Pereval_areas(Base):
    __tablename__ = "pereval_areas"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_parent = Column(Integer, index=True)
    title = Column(String)

class Pereval_images(Base):
    __tablename__ = "pereval_images"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_added = Column(DateTime)
    img = Column(BINARY)

class Spr_activities_types(Base):
    __tablename__ = "spr_activities_types"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)

SessionLocal = sessionmaker(autoflush=False, bind=engine)