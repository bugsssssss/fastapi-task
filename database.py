# database.py
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from pydantic import BaseModel


DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    username = Column(String, index=True, unique=True)
    password = Column(String)


# Создание таблицы
Base.metadata.create_all(bind=engine)

# Создание сессии 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
