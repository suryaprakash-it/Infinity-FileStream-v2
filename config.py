import os
from dotenv import load_dotenv

load_dotenv()

# 1. Logic is performed outside the class
api_id = int(os.getenv("API_ID", 0))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
mongo_uri = os.getenv("MONGO_URI")
base_url = os.getenv("BASE_URL")
storage_chat_id = int(os.getenv("STORAGE_CHAT_ID", -1004309324849))
admins_str = os.getenv("ADMINS", "")
admins = [int(x) for x in admins_str.split() if x]

# 2. Validation
if not all([api_id, api_hash, bot_token, mongo_uri, base_url]):
    raise ValueError("❌ Missing critical environment variables (API_ID, API_HASH, BOT_TOKEN, MONGO_URI, or BASE_URL)!")

# 3. Clean Class Definition
class Config:
    API_ID = api_id
    API_HASH = api_hash
    BOT_TOKEN = bot_token
    MONGO_URI = mongo_uri
    BASE_URL = base_url
    STORAGE_CHAT_ID = storage_chat_id
    ADMINS = admins
