from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# បង្កើត SQLAlchemy engine (ភ្ជាប់ទៅកាន់ Database)
engine = create_engine(settings.DATABASE_URL)

# បង្កើត Session factory សម្រាប់ប្រើប្រាស់ពេលមាន Request ម្តងៗ
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class សម្រាប់ឱ្យ Models របស់យើងទាញយកមកប្រើ
Base = declarative_base()

# Dependency សម្រាប់ទាញយក database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()