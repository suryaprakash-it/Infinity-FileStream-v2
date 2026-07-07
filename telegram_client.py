from pyrogram import Client
from config import Config
import os

# Use the environment variable to keep your session string secure
bot = Client(
    "bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    session_string=os.getenv("SESSION_STRING") 
)
