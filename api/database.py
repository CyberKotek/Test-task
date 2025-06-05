import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_CONNECTION = os.environ["DB_CONNECTION"]

engine = create_engine(DB_CONNECTION)

SessionLoacal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db = SessionLoacal()
    try:
        yield db
    finally:
        db.close()
