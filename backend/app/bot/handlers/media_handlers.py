import os
from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

from app.services.transcription import transcribe_audio
from app.services.gemini import ask_gemini  # <-- Import មុខងារថ្មីបញ្ជូនទៅ AI
from app.services.tts import text_to_speech # Import មុខងារ Text-to-Speech
from app.db.database import SessionLocal       # <-- NEW IMPORT
from app.db.crud import log_user_and_transcription # <-- NEW IMPORT

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    """Handle /start command."""
    await message.reply(
        "👋 *Whisper Transcription Bot*\n\n"
        "Send me any of the following and I'll transcribe it:\n\n"
        "🎙️ Voice messages\n"
        "🎵 Audio files (MP3, WAV, OGG, etc.)\n"
        "🎥 Video files (MP4, MKV, WEBM, etc.)\n"
        "📹 Video notes\n"
        "📎 Document files (audio/video)\n\n"
        "Just send the file and I'll get to work!",
        parse_mode="Markdown"
    )

@router.message(F.voice)
async def handle_voice_message(message: Message, bot: Bot):
    processing_msg = await message.reply("🎧 ទីតាំងសំឡេងទទួលបាន! កំពុងបំប្លែងទៅជាអត្ថបទ...\n*(Processing audio...)*", parse_mode="Markdown")
    
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    temp_filename = f"temp_voice_{file_id}.ogg"
    
    try:
        # Download and transcribe
        await bot.download_file(file.file_path, destination=temp_filename)
        transcribed_text = await transcribe_audio(temp_filename)
        
        # --- NEW: Save the results to PostgreSQL ---
        # We open a brief database session, save the data, and close it.
        with SessionLocal() as db:
            log_user_and_transcription(
                db=db,
                telegram_id=str(message.from_user.id),
                full_name=message.from_user.full_name,
                text=transcribed_text,
                file_type="voice"
            )
        # -------------------------------------------
        
        # ប្រសិនបើមានមនុស្សនិយាយមែន ទើបបញ្ជូនទៅសួរ AI
        if "គ្មានសំឡេងមនុស្សនិយាយទេ" not in transcribed_text:
            # ២. Update សារប្រាប់អ្នកប្រើប្រាស់ថា AI កំពុងគិត
            await processing_msg.edit_text(f"🗣️ **អ្នកបញ្ជា:** {transcribed_text}\n\n🤖 *កំពុងគិតរកចម្លើយ...* (Thinking...)", parse_mode="Markdown")
            
            # ៣. បញ្ជូនអត្ថបទទៅកាន់ Gemini 
            ai_answer = await ask_gemini(transcribed_text)
            
            # ៤. ផ្ញើចម្លើយចុងក្រោយត្រឡប់ទៅអ្នកប្រើប្រាស់
            final_reply = f"🗣️ **អ្នក:** {transcribed_text}\n\n🤖 **AI:** {ai_answer}"
            await processing_msg.edit_text(final_reply, parse_mode="Markdown")
            
            # --- ផ្នែកថ្មី៖ បំប្លែងចម្លើយ AI ទៅជាសំឡេង ---
            voice_status_msg = await message.reply("🎙️ *កំពុងថតសំឡេងតបត...*", parse_mode="Markdown")
            
            # កាត់អត្ថបទយកត្រឹម ៥០០ អក្សរដំបូង
            short_answer = ai_answer[:500]
            
            # បំប្លែងអក្សរទៅជា File សំឡេង (.mp3)
            audio_file = await text_to_speech(short_answer, lang='km')
            
            if audio_file:
                voice_msg = FSInputFile(audio_file)
                await message.reply_voice(voice=voice_msg)
                os.remove(audio_file)
                
            await voice_status_msg.delete()
            
        else:
            # បើគ្មានសំឡេងមនុស្សទេ ផ្ញើតែអត្ថបទនោះទៅបានហើយ
            await processing_msg.edit_text(f"📝 **លទ្ធផល:**\n{transcribed_text}", parse_mode="Markdown")
        
    except Exception as e:
        await processing_msg.edit_text(f"❌ មានបញ្ហា (Error): {str(e)}")
        
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

@router.message(F.video | F.video_note)
async def handle_video_message(message: Message, bot: Bot):
    processing_msg = await message.reply("📹 ទីតាំងវីដេអូទទួលបាន! កំពុងបំប្លែងទៅជាអត្ថបទ...\n*(Processing video...)*", parse_mode="Markdown")
    if message.video:
        file_id = message.video.file_id
    else:
        file_id = message.video_note.file_id
    file = await bot.get_file(file_id)
    temp_filename = f"temp_video_{file_id}.mp4"
    try:
        await bot.download_file(file.file_path,destination = temp_filename)
        transcribed_text = await transcribe_audio(temp_filename)
        with SessionLocal() as db:
            log_user_and_transcription(
                db=db,
                telegram_id=str(message.from_user.id),
                full_name=message.from_user.full_name,
                text=transcribed_text,
                file_type="video"
            )
            
        # ប្រសិនបើមានមនុស្សនិយាយមែន ទើបបញ្ជូនទៅសួរ AI
        if "គ្មានសំឡេងមនុស្សនិយាយទេ" not in transcribed_text:
            # ២. Update សារប្រាប់អ្នកប្រើប្រាស់ថា AI កំពុងគិត
            await processing_msg.edit_text(f"🗣️ **អ្នកបញ្ជា:** {transcribed_text}\n\n🤖 *កំពុងគិតរកចម្លើយ...* (Thinking...)", parse_mode="Markdown")
            
            # ៣. បញ្ជូនអត្ថបទទៅកាន់ Gemini 
            ai_answer = await ask_gemini(transcribed_text)
            
            # ៤. ផ្ញើចម្លើយចុងក្រោយត្រឡប់ទៅអ្នកប្រើប្រាស់
            final_reply = f"🗣️ **អ្នក:** {transcribed_text}\n\n🤖 **AI:** {ai_answer}"
            await processing_msg.edit_text(final_reply, parse_mode="Markdown")
            
            # --- ផ្នែកថ្មី៖ បំប្លែងចម្លើយ AI ទៅជាសំឡេង ---
            voice_status_msg = await message.reply("🎙️ *កំពុងថតសំឡេងតបត...*", parse_mode="Markdown")
            
            short_answer = ai_answer[:500]
            audio_file = await text_to_speech(short_answer, lang='km')
            
            if audio_file:
                voice_msg = FSInputFile(audio_file)
                await message.reply_voice(voice=voice_msg)
                os.remove(audio_file)
                
            await voice_status_msg.delete()
            
        else:
            # បើគ្មានសំឡេងមនុស្សទេ ផ្ញើតែអត្ថបទនោះទៅបានហើយ
            await processing_msg.edit_text(f"📝 **លទ្ធផល:**\n{transcribed_text}", parse_mode="Markdown")
    except Exception as e:
        await processing_msg.edit_text(f"❌ មានបញ្ហា (Error): {str(e)}")
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

    