from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    full_name = Column(String)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

class Transcription(Base):
    __tablename__ = "transcriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, ForeignKey("users.telegram_id"))
    transcribed_text = Column(Text)
    file_type = Column(String) # 'voice' ឬ 'video'
    created_at = Column(DateTime(timezone=True), server_default=func.now())