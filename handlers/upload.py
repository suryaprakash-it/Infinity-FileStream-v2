from pyrogram import filters
from secrets import token_urlsafe
import os

from database import files
from config import Config


async def upload_handler(client, message):

    media = (
        message.document
        or message.video
        or message.audio
        or message.photo
    )

    if not media:
        return

    # Copy message to storage group
    copied = await message.copy(Config.STORAGE_CHAT_ID)

    storage_media = (
        copied.document
        or copied.video
        or copied.audio
        or copied.photo
    )

    if copied.document:
        file_name = copied.document.file_name

    elif copied.video:
        file_name = copied.video.file_name or f"{copied.id}.mp4"

    elif copied.audio:
        file_name = copied.audio.file_name or f"{copied.id}.mp3"

    elif copied.photo:
        file_name = f"{copied.id}.jpg"

    else:
        file_name = "file"

    file_size = storage_media.file_size

    file_code = token_urlsafe(6)

    await files.insert_one({
        "_id": file_code,
        "chat_id": copied.chat.id,
        "message_id": copied.id,
        "file_name": file_name,
        "file_size": file_size
    })

    link = f"{Config.BASE_URL}/file/{file_code}"

    await message.reply_text(
        f"✅ File Stored!\n\n"
        f"📄 {file_name}\n"
        f"📦 {file_size} bytes\n\n"
        f"🔗 {link}"
    )


def register(app):
    app.on_message(
        filters.document
        | filters.video
        | filters.audio
        | filters.photo
    )(upload_handler)