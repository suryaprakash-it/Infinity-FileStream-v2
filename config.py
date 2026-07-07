import os
from dotenv import load_dotenv

load_dotenv()

# 1. Fetch variables (use None as default to properly detect missing values)
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
mongo_uri = os.getenv("MONGO_URI")
base_url = os.getenv("BASE_URL")
storage_chat_id = os.getenv("STORAGE_CHAT_ID", "-1004309324849")
admins_str = os.getenv("ADMINS", "")

# 2. Validation: Check if required variables exist as strings
required_vars = {
    "API_ID": api_id,
    "API_HASH": api_hash,
    "BOT_TOKEN": bot_token,
    "MONGO_URI": mongo_uri,
    "BASE_URL": base_url
}

missing = [key for key, value in required_vars.items() if not value]

if missing:
    raise ValueError(f"❌ Missing critical environment variables: {', '.join(missing)}")

# 3. Safe conversion after validation
class Config:
    API_ID = int(api_id)
    API_HASH = api_hash
    BOT_TOKEN = bot_token
    MONGO_URI = mongo_uri
    BASE_URL = base_url.rstrip('/')  # Ensure no trailing slash
    STORAGE_CHAT_ID = int(storage_chat_id)
    ADMINS = [int(x) for x in admins_str.split() if x]
