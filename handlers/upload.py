from pyrogram import filters
from secrets import token_urlsafe
import math

from database import files
from config import Config

# Helper function to convert raw bytes into human-readable sizes (KB, MB, GB)
def format_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

async def upload_handler(client, message):
    # Added quote=False to remove the reply box, and updated to a cooler status message
    status_msg = await message.reply_text("⏳ **Initializing Upload Sequence...**", quote=False)
    
    media = (message.document or message.video or message.audio or message.photo)

    if not media:
        await status_msg.edit_text("❌ **Upload Failed:** No valid media found.")
        return

    try:
        target_id = int(Config.STORAGE_CHAT_ID)
        chat = await client.get_chat(target_id)
        copied = await message.copy(chat.id)

        storage_media = (copied.document or copied.video or copied.audio or copied.photo)

        if copied.document:
            file_name = copied.document.file_name
        elif copied.video:
            file_name = copied.video.file_name or f"video_{copied.id}.mp4"
        elif copied.audio:
            file_name = copied.audio.file_name or f"audio_{copied.id}.mp3"
        elif copied.photo:
            file_name = f"photo_{copied.photo.file_unique_id[:8]}.jpg"
        else:
            file_name = "file"

        file_size = storage_media.file_size

        while True:
            file_code = token_urlsafe(6)
            if not await files.find_one({"_id": file_code}):
                break

        await files.insert_one({
            "_id": file_code,
            "chat_id": copied.chat.id,
            "message_id": copied.id,
            "file_name": file_name,
            "file_size": file_size
        })

        link = f"{Config.BASE_URL}/file/{file_code}"
        readable_size = format_size(file_size)

        # Sleek, branded output message
        await status_msg.edit_text(
            f"⚡️ **INFINITY UPLOAD COMPLETE** ⚡️\n\n"
            f"📁 **Name:** {file_name}\n"
            f"📊 **Size:** {readable_size}\n\n"
            f"🔗 **Direct Link:**\n{link}"
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        await status_msg.edit_text(f"❌ **System Error:** Copy Failed!\n\n`{e}`")

def register(app):
    # Added filters.private so it only responds in DMs, keeping groups clean
    app.on_message(
        (filters.document | filters.video | filters.audio | filters.photo) & filters.private
    )(upload_handler)
