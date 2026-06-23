import os 
from dotenv import load_dotenv


load_dotenv()
class Setting:
    BOT_TOKEN:str = os.getenv('BOT_TOKEN')
    DATABASE_URL:str = os.getenv('DATABASE_URL')
    WHISPER_MODEL:str = os.getenv('WHISPER_MODEL')
settings = Setting()
