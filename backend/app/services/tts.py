import os
import uuid
import asyncio
from gtts import gTTS

def _generate_audio_sync(text: str, filename: str, lang: str):
    """មុខងារសម្រាប់ទាញយកសំឡេងពី Google (រត់ជា Sync)"""
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(filename)

async def text_to_speech(text: str, lang: str = 'km') -> str:
    """មុខងារ Async ដើម្បីកុំឱ្យ Bot គាំងពេលកំពុងបំប្លែងសំឡេង"""
    try:
        # បង្កើតឈ្មោះ File ថ្មីកុំឱ្យជាន់គ្នាពេលមានអ្នកប្រើច្រើន
        filename = f"temp_reply_{uuid.uuid4().hex}.mp3"
        
        # ប្រើប្រាស់ Thread ដើម្បីដំណើរការ gTTS ដោយមិនឱ្យគាំង Server
        await asyncio.to_thread(_generate_audio_sync, text, filename, lang)
        
        return filename
    except Exception as e:
        print(f"⚠️ មានបញ្ហាក្នុងការបំប្លែងសំឡេង: {e}")
        return None
