import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    MONGO_URI = os.getenv("MONGO_URI")

    BASE_URL = os.getenv("BASE_URL")

    ADMINS = [
        int(x)
        for x in os.getenv("ADMINS", "").split()
        if x
    ]