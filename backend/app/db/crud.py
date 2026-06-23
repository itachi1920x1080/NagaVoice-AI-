from sqlalchemy.orm import Session
from app.db.models import User, Transcription

def log_user_and_transcription(db: Session, telegram_id: str, full_name: str, text: str, file_type: str = "voice"):
    """Saves the user (if new) and logs their transcription."""
    
    # 1. Check if the user already exists in the database
    user = db.query(User).filter(User.telegram_id == str(telegram_id)).first()
    
    # 2. If they are new, add them to the users table
    if not user:
        user = User(telegram_id=str(telegram_id), full_name=full_name)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # 3. Add the transcription text to the transcriptions table
    new_record = Transcription(
        telegram_id=str(telegram_id),
        transcribed_text=text,
        file_type=file_type
    )
    db.add(new_record)
    db.commit()