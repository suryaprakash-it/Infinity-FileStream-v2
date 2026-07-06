from pyrogram import filters
from database import files
from secrets import token_urlsafe
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

    file_id = media.file_id
    file_name = getattr(media, "file_name", "Photo")
    file_size = media.file_size

    uid = token_urlsafe(6)

    await files.insert_one({
        "_id": uid,
        "file_id": file_id,
        "file_name": file_name
    })

    link = f"{Config.BASE_URL}/file/{uid}"

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