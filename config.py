import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    try:
        API_ID = int(os.getenv("API_ID", 0))
        API_HASH = os.getenv("API_HASH")
        BOT_TOKEN = os.getenv("BOT_TOKEN")
        MONGO_URI = os.getenv("MONGO_URI")
        BASE_URL = os.getenv("BASE_URL")
        STORAGE_CHAT_ID = int(os.getenv("STORAGE_CHAT_ID", -1004309324849))
        
        ADMINS = [int(x) for x in os.getenv("ADMINS", "").split() if x]

        # Validation: Ensure critical values exist
        if not all([API_ID, API_HASH, BOT_TOKEN, MONGO_URI, BASE_URL]):
            raise ValueError("Missing critical environment variables!")
            
    except Exception as e:
        print(f"❌ Configuration Error: {e}")
        raise e
