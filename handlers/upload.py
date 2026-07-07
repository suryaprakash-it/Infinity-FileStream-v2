from pyrogram import filters
from secrets import token_urlsafe

from database import files
from config import Config

async def upload_handler(client, message):
    # 1. Provide immediate feedback
    status_msg = await message.reply_text("⏳ Processing your file...")

    # 2. Identify the media
    media = (
        message.document
        or message.video
        or message.audio
        or message.photo
    )

    if not media:
        await status_msg.edit_text("❌ No valid media found.")
        return

    try:
        # 3. Copy to storage channel - ENSURE ID IS INT
        target_chat = int(Config.STORAGE_CHAT_ID)
        copied = await message.copy(target_chat)
        
        # 4. Determine media properties from the stored copy
        storage_media = (
            copied.document
            or copied.video
            or copied.audio
            or copied.photo
        )

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

        # 5. Generate a guaranteed unique file code
        while True:
            file_code = token_urlsafe(6)
            if not await files.find_one({"_id": file_code}):
                break

        # 6. Save to database
        await files.insert_one({
            "_id": file_code,
            "chat_id": copied.chat.id,
            "message_id": copied.id,
            "file_name": file_name,
            "file_size": file_size
        })

        # 7. Generate link and update user
        link = f"{Config.BASE_URL}/file/{file_code}"
        
        await status_msg.edit_text(
            f"✅ **File Stored!**\n\n"
            f"📄 `{file_name}`\n"
            f"📦 `{file_size} bytes`\n\n"
            f"🔗 {link}"
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        await status_msg.edit_text(f"❌ Copy Failed!\n\n`{e}`")

def register(app):
    app.on_message(
        filters.document
        | filters.video
        | filters.audio
        | filters.photo
    )(upload_handler)
