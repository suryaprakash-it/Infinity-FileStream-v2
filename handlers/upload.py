from pyrogram import filters

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

    await message.reply_text(
        f"✅ File Received!\n\n"
        f"📄 {file_name}\n"
        f"📦 {file_size} bytes"
    )


def register(app):
    app.on_message(
        filters.document
        | filters.video
        | filters.audio
        | filters.photo
    )(upload_handler)