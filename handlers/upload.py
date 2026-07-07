from pyrogram import filters
from secrets import token_urlsafe

from database import files
from config import Config


async def upload_handler(client, message):

    print("1️⃣ Upload received")

    media = (
        message.document
        or message.video
        or message.audio
        or message.photo
    )

    if not media:
        print("❌ No media")
        return

    try:
        print("2️⃣ Copying to storage...")

        copied = await message.copy(Config.STORAGE_CHAT_ID)

        print("3️⃣ Copy completed")
        print("Storage Chat ID:", copied.chat.id)
        print("Storage Message ID:", copied.id)

    except Exception as e:
        import traceback
        traceback.print_exc()

        await message.reply_text(
            f"❌ Copy Failed!\n\n{e}"
        )
        return

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

    print("4️⃣ Saving to MongoDB...")

    await files.insert_one({
        "_id": file_code,
        "chat_id": copied.chat.id,
        "message_id": copied.id,
        "file_name": file_name,
        "file_size": file_size
    })

    print("5️⃣ MongoDB saved")

    link = f"{Config.BASE_URL}/file/{file_code}"

    print("6️⃣ Sending reply...")

    await message.reply_text(
        f"✅ File Stored!\n\n"
        f"📄 {file_name}\n"
        f"📦 {file_size} bytes\n\n"
        f"🔗 {link}"
    )

    print("7️⃣ Done")


def register(app):
    app.on_message(
        filters.document
        | filters.video
        | filters.audio
        | filters.photo
    )(upload_handler)