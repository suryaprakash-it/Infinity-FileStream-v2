import string
import random
from pyrogram import Client, filters
from database import files
from config import Config

# Helper to generate a random 8-character code
def generate_short_code(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def register_handlers(bot: Client):
    
    @bot.on_message(filters.document | filters.video | filters.audio)
    async def handle_file(client, message):
        media = message.document or message.video or message.audio
        # Telegram's unique ID ensures we identify the same file across different messages
        file_unique_id = media.file_unique_id 
        
        # 1. Look for the file in the database using the unique ID
        existing_file = await files.find_one({"file_unique_id": file_unique_id})
        
        if existing_file:
            # Reusing the existing link for the same file
            file_code = existing_file["_id"]
            link = f"{Config.BASE_URL}/file/{file_code}"
            await message.reply(f"🔗 **Already exists:**\n\n{link}")
            
        else:
            # 2. Create a new entry if it's the first time we see this file
            file_code = generate_short_code()
            
            await files.insert_one({
                "_id": file_code,
                "file_unique_id": file_unique_id, 
                "file_name": getattr(media, "file_name", "Unknown_File"),
                "file_size": media.file_size,
                "chat_id": message.chat.id,
                "message_id": message.id
            })
            
            link = f"{Config.BASE_URL}/file/{file_code}"
            await message.reply(f"✅ **New permanent link generated:**\n\n{link}")
