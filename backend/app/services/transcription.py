import os
from groq import AsyncGroq

# ទាញយក API Key ពី File .env ឬ Render Environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# បង្កើត Client សម្រាប់តភ្ជាប់ទៅកាន់ Groq
client = AsyncGroq(api_key=GROQ_API_KEY)

async def transcribe_audio(file_path: str) -> str:
    """បំប្លែងសំឡេងទៅជាអត្ថបទដោយប្រើ Groq API (ល្បឿនផ្លេកបន្ទោរ)"""
    try:
        # បើក File សំឡេងដែលទទួលបានពី Telegram
        with open(file_path, "rb") as file:
            # បញ្ជូនសំឡេងទៅកាន់ Groq Whisper Model
            transcription = await client.audio.transcriptions.create(
                file=(file_path, file.read()), # បញ្ជូនឈ្មោះ និងទិន្នន័យ File
                model="whisper-large-v3-turbo", # ម៉ូដែលចុងក្រោយ លឿនបំផុត
                prompt="អត្ថបទនេះជាភាសាខ្មែរ (Khmer language).", # ជួយប្រាប់ AI ឱ្យដឹងមុនថាជាភាសាខ្មែរ
                response_format="text"
            )
            
        return transcription
    except Exception as e:
        print(f"⚠️ Groq Error: {e}")
        return ""