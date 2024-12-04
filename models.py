from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String,DateTime,BINARY,Float,ForeignKey

from fastapi import FastAPI

SQLALCHEMY_DATABASE_URL = "sqlite:///db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

class Base(DeclarativeBase): pass


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
    title = Column(String)

class Spr_activities_types(Base):
    __tablename__ = "spr_activities_types"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)

class Users(Base):
    __tablename__ = "users"
    id    = Column(
            Integer,
            primary_key=True,
            index=True,
            autoincrement=True)
    email = Column(String)
    phone = Column(String)
    fam   = Column(String)
    name  = Column(String)
    otc   = Column(String)

class Choords(Base):
    __tablename__ = "choords"
    id = Column(Integer,
                primary_key=True,
                index=True,
                autoincrement=True)
    latitude  = Column(Float, index=True)
    longitude = Column(Float, index=True)
    height    = Column(Integer, index=True)


class Pereval_added(Base):
    __tablename__ = "pereval_added"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_added   = Column(DateTime)
    beautyTitle  = Column(String)
    title        = Column(String)
    other_titles = Column(String)
    connect      = Column(String)
    level_winter = Column(String)
    level_summer = Column(String)
    level_autumn = Column(String)
    level_spring = Column(String)
    user = Column(Integer, ForeignKey(Users.id))
    choords = Column(Integer, ForeignKey(Choords.id))


class Pereval_pereval_images(Base):
    __tablename__ = "pereval_pereval_images"
    id            = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_pereval    = Column(Integer, ForeignKey(Pereval_added.id), index=True)
    id_image      = Column(Integer, ForeignKey(Pereval_images.id), index=True)


SessionLocal = sessionmaker(autoflush=False, bind=engine)
