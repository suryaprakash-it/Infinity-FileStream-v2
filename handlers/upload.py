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

    file_name = getattr(media, "file_name", "Photo")
    file_size = media.file_size

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