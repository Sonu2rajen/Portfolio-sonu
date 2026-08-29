from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from sqlalchemy.orm import Session
from fastapi import Depends

DATABASE_URL = "sqlite:///resume_parser.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
