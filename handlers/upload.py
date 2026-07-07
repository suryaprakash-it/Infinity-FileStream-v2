from pyrogram import filters
from secrets import token_urlsafe

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

    # Get correct filename and file size
    if message.document:
        file_name = message.document.file_name
        file_size = message.document.file_size

    elif message.video:
        file_name = message.video.file_name or f"{message.id}.mp4"
        file_size = message.video.file_size

    elif message.audio:
        file_name = message.audio.file_name or f"{message.id}.mp3"
        file_size = message.audio.file_size

    elif message.photo:
        file_name = f"{message.id}.jpg"
        file_size = message.photo.file_size

    else:
        file_name = "file"
        file_size = 0

    file_code = token_urlsafe(6)

    await files.insert_one({
        "_id": file_code,
        "chat_id": message.chat.id,
        "message_id": message.id,
        "file_name": file_name,
        "file_size": file_size
    })

    link = f"{Config.BASE_URL}/file/{file_code}"

    await message.reply_text(
        f"✅ File Uploaded!\n\n"
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