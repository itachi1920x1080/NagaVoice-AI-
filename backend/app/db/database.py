import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# ទាញយកទិន្នន័យពី .env
load_dotenv() 

# ទាញយក DATABASE_URL បើគ្មានវាទេ វានឹងប្រើ sqlite ជំនួស (ដើម្បីការពារ Error)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

# បង្កើត Engine សម្រាប់ភ្ជាប់ទៅ PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()