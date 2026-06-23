import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from aiogram import Bot, Dispatcher, types
from app.bot.handlers import media_handlers, commands
from app.core.config import settings
from app.db.database import engine, Base, get_db
from app.db.models import User, Transcription
from app.db import models  # ដើម្បីប្រាកដថា Models ត្រូវបាន load ចូល
# 1. Initialize Aiogram Bot and Dispatcher
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(commands.router)       # Commands ដើរមុនគេ
dp.include_router(media_handlers.router) # បន្ទាប់មកទើបចាំទទួលសំឡេង/វីដេអូ

# 2. Define Lifespan for Background Tasks
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup Logic ---
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Starting Telegram Bot polling...")
    # Run bot polling as a background task so it doesn't block FastAPI
    bot_task = asyncio.create_task(dp.start_polling(bot))
    
    yield  # The application runs here while yielding control
    
    # --- Shutdown Logic ---
    print("Stopping Telegram Bot polling...")
    await bot.session.close()
    bot_task.cancel()
    try:
        await bot_task
    except asyncio.CancelledError:
        print("Bot polling task successfully closed.")

# 3. Initialize FastAPI with Lifespan
app = FastAPI(
    title="NagaVoice AI API",
    version="1.0.0",
    lifespan=lifespan
)

# 4. Configure CORS for your Vue 3 Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # អនុញ្ញាតគ្រប់ IP ទាំងអស់ (សម្រាប់ពេលសរសេរកូដ)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the NagaVoice AI API!"}

# 5. Basic Health Check Route
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "bot_connected": bool(settings.BOT_TOKEN)}

# 6. Dashboard Stats Endpoint
@app.get("/api/dashboard-stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """ទាញយកស្ថិតិសរុបសម្រាប់បង្ហាញលើ Web Dashboard"""
    
    total_users = db.query(User).count()
    total_transcriptions = db.query(Transcription).count()
    
    voice_count = db.query(Transcription).filter(Transcription.file_type == "voice").count()
    video_count = db.query(Transcription).filter(Transcription.file_type == "video").count()
    
    return {
        "total_users": total_users,
        "total_transcriptions": total_transcriptions,
        "voice_count": voice_count,
        "video_count": video_count
    }

# 7. Dashboard History Endpoint
@app.get("/api/dashboard-history")
def get_dashboard_history(db: Session = Depends(get_db)):
    """ទាញយកប្រវត្តិនៃការបំប្លែងចុងក្រូយចំនួន ១០ ដើម្បីបង្ហាញក្នុងតារាង"""
    
    # ទាញយកទិន្នន័យ Transcription ព្រមទាំងភ្ជាប់ជាមួយទិន្នន័យ User (អ្នកផ្ញើ) ផងដែរ
    recent_history = db.query(Transcription).join(User).order_by(
        desc(Transcription.created_at)
    ).limit(10).all()
    
    # រៀបចំទិន្នន័យជាទម្រង់ JSON ដើម្បីបញ្ជូនទៅ Frontend
    history_data = []
    for item in recent_history:
        # ស្វែងរកឈ្មោះអ្នកប្រើប្រាស់ពីទំនាក់ទំនង Database
        user_name = db.query(User).filter(User.telegram_id == item.telegram_id).first()
        
        history_data.append({
            "id": item.id,
            "full_name": user_name.full_name if user_name else "Unknown",
            "file_type": item.file_type,
            "text": item.transcribed_text,
            "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S") if item.created_at else "N/A"
        })
        
    return history_data
