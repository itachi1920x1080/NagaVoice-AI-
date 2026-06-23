from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import desc

# នាំចូល Database Session និង Models របស់អ្នក
# (សូមប្រាកដថាផ្លូវ Import នេះត្រឹមត្រូវតាមរចនាសម្ព័ន្ធ Folder របស់អ្នក)
from app.db.database import SessionLocal
from app.db.models import User, Transcription

router = Router()

@router.message(Command("start", "help"))
async def cmd_start(message: types.Message):
    """ដំណើរការនៅពេលអ្នកប្រើប្រាស់វាយ /start ឬ /help"""
    welcome_text = (
        "👋 **សួស្តី! ខ្ញុំជា NagaVoice AI Assistant**\n\n"
        "សូមផ្ញើសារសំឡេង ឬវីដេអូមកខ្ញុំ ខ្ញុំនឹងបំប្លែងវាជាអក្សរ ហើយឆ្លើយតបទៅអ្នកវិញភ្លាមៗ!\n\n"
        "**ពាក្យបញ្ជាដែលមាន៖**\n"
        "🔹 /start - មើលការណែនាំនេះ\n"
        "🔹 /stats - មើលស្ថិតិប្រើប្រាស់របស់អ្នក\n"
        "🔹 /history - មើលប្រវត្តិសំណួរចាស់ៗរបស់អ្នក"
    )
    await message.reply(welcome_text, parse_mode="Markdown")

@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    """ទាញយកស្ថិតិពិតប្រាកដពី PostgreSQL Database"""
    user_id = str(message.from_user.id)
    
    # បើកការតភ្ជាប់ទៅកាន់ Database
    with SessionLocal() as db:
        # រាប់ចំនួនសរុបដែល User នេះបានបំប្លែងសំឡេង
        total_transcriptions = db.query(Transcription).filter(
            Transcription.telegram_id == user_id
        ).count()
        
        # រាប់បំបែកតាមប្រភេទ File (Voice ឫ Video)
        voice_count = db.query(Transcription).filter(
            Transcription.telegram_id == user_id,
            Transcription.file_type == 'voice'
        ).count()
        
        video_count = db.query(Transcription).filter(
            Transcription.telegram_id == user_id,
            Transcription.file_type == 'video'
        ).count()

    stats_text = (
        f"📊 **ស្ថិតិរបស់អ្នក (ID: {user_id})**\n\n"
        f"✅ ប្រតិបត្តិការសរុប: `{total_transcriptions} ដង`\n"
        f"🎙️ សារសំឡេង (Voice): `{voice_count} ដង`\n"
        f"🎥 វីដេអូ (Video): `{video_count} ដង`"
    )
    await message.reply(stats_text, parse_mode="Markdown")

@router.message(Command("history"))
async def cmd_history(message: types.Message):
    """ទាញយកប្រវត្តិ ៥ ដងចុងក្រោយពី PostgreSQL Database"""
    user_id = str(message.from_user.id)
    
    with SessionLocal() as db:
        # ទាញយកទិន្នន័យ ៥ ចុងក្រោយគេបង្អស់ តម្រៀបតាមម៉ោង (ថ្មីមុន ចាស់ក្រោយ)
        recent_transcriptions = db.query(Transcription).filter(
            Transcription.telegram_id == user_id
        ).order_by(desc(Transcription.created_at)).limit(5).all()

    if not recent_transcriptions:
        await message.reply("📭 អ្នកមិនទាន់មានប្រវត្តិប្រើប្រាស់នៅឡើយទេ។", parse_mode="Markdown")
        return

    history_text = "📜 **ប្រវត្តិ ៥ ដងចុងក្រោយរបស់អ្នក៖**\n\n"
    
    # វដ្ត (Loop) ដើម្បីទាញអត្ថបទមកបង្ហាញជាជួរ
    for index, record in enumerate(recent_transcriptions, start=1):
        # កាត់អត្ថបទឱ្យខ្លី បើវាវែងពេក (បង្ហាញត្រឹម ៥០ អក្សរដំបូង)
        text_preview = record.transcribed_text
        if len(text_preview) > 50:
            text_preview = text_preview[:50] + "..."
            
        history_text += f"{index}️⃣ _{text_preview}_\n"

    await message.reply(history_text, parse_mode="Markdown")