from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.configs import settings
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = settings.DB_ADDRESS
engine=create_engine(SQLALCHEMY_DATABASE_URL)
session=sessionmaker(bind=engine)
Base=declarative_base()
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()