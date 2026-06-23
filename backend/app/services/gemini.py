import os
from google import genai

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

async def ask_gemini(text_prompt: str) -> str:
    """បញ្ជូនអត្ថបទទៅសួរ Gemini ហើយបង្ខំឱ្យឆ្លើយជាភាសាខ្មែរជានិច្ច"""
    try:
        # បន្ថែម System Prompt នៅពីមុខអត្ថបទរបស់អ្នកប្រើប្រាស់
        # នេះជាការបញ្ជាដាច់ខាតទៅកាន់ AI ឱ្យប្រើប្រាស់តែភាសាខ្មែរ
        strict_prompt = (
            "You are NagaVoice, a highly intelligent and helpful AI assistant for Cambodian users. "
            "IMPORTANT RULE: You MUST always reply strictly in the Khmer language (ភាសាខ្មែរ), "
            "no matter what language the user speaks or what text is provided. "
            f"Here is the user's input: {text_prompt}"
        )
        
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=strict_prompt,
        )
        return response.text
    except Exception as e:
        return f"⚠️ សុំទោស មានបញ្ហាក្នុងការតភ្ជាប់ទៅកាន់ AI: {str(e)}"