from pyrogram import Client
from config import Config
import os

# The bot will now use the string session instead of creating a file
bot = Client(
    "bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    session_string=os.getenv("BQAeORcAmgVLl_iBa378uNagwtHxmIpVdoJDddbEVDcqm7WJS2JD2ClYkASPbwX2b5GJ_9lxYkgTchCyQWVkNBvrnt9n6vpJ_semPiiUk59Qa3l1Z29S4SscCw9qsi38Lnee3JjuuosMkt0CJRiTTHvXn8TOV5v-nFICpyBvBf0lpd-JKq2ot2kcerOhDk5lQ-vbdryEncwiWIUhCoIGqXp96Nny2My1649bPSCmhc-PsiLwzg3nEAp0d_MdSath_nPy6ADAA8twkXEFXUn97ropX-Bo1rq2uv15sZD4nsk1VnCRGYFIhpBeJV9EA1zBh-h6SbdYOJ_oAHcy7uEWzmoSSZGwzwAAAABrlaseAA")
)
