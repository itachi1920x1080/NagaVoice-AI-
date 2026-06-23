import os
import asyncio # ត្រូវបន្ថែមការ Import នេះ
from google import genai

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

async def ask_gemini(text_prompt: str, retries: int = 3) -> str:
    """បញ្ជូនអត្ថបទទៅសួរ Gemini ហើយមានមុខងារសាកល្បងម្តងទៀតបើគាំង"""
    
    strict_prompt = (
        "You are NagaVoice, a highly intelligent and helpful AI assistant for Cambodian users. "
        "IMPORTANT RULE: You MUST always reply strictly in the Khmer language (ភាសាខ្មែរ). "
        f"Here is the user's input: {text_prompt}"
    )
    
    # ឱ្យវាសាកល្បងសួរចំនួន ៣ ដង បើបរាជ័យ
    for attempt in range(retries):
        try:
            response = await client.aio.models.generate_content(
                model='gemini-2.5-flash',
                contents=strict_prompt,
            )
            return response.text
            
        except Exception as e:
            error_msg = str(e)
            # បើ Error នោះគឺ 503 (Server រវល់) ហើយវាមិនទាន់អស់ជុំ
            if "503" in error_msg and attempt < retries - 1:
                print(f"⚠️ Google Server រវល់, កំពុងព្យាយាមម្តងទៀតលើកទី {attempt + 1}...")
                await asyncio.sleep(2) # សម្រាក ២ វិនាទីសិន ចាំសួរម្តងទៀត
                continue # ត្រលប់ទៅដើមរង្វិលជុំ
                
            # បើសាក ៣ ដងហើយនៅតែមិនបាន ឬជា Error ផ្សេង
            return f"⚠️ សុំទោស ពេលនេះប្រព័ន្ធ AI កំពុងរវល់ខ្លាំង។ សូមសាកល្បងម្តងទៀតនៅពេលបន្តិចទៀតនេះ។"