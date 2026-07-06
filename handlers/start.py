from hydrogram import filters

async def start_handler(client, message):
    await message.reply_text(
        "👋 Welcome to Infinity FileStream!\n\nSend me any file."
    )

def register(app):
    app.on_message(filters.command("start"))(start_handler)