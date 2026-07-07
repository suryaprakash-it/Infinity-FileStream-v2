from pyrogram import filters

async def start_handler(client, message):
    # Grab the user's first name for a personalized touch (defaults to 'User' if hidden)
    user_name = message.from_user.first_name if message.from_user else "User"

    # A stylish, Markdown-formatted welcome message
    welcome_text = (
        f"🚀 **Welcome to Infinity FileStream, {user_name}!**\n\n"
        f"I am a high-performance, stateless file streaming engine. ⚡️\n\n"
        f"**How to use me:**\n"
        f"1️⃣ Send me any **Document, Video, Audio,** or **Photo**.\n"
        f"2️⃣ I will instantly secure it in my cloud vault. 🛡️\n"
        f"3️⃣ I will generate a direct, high-speed download link for you! 🔗\n\n"
        f"👇 **Drop a file below to initiate upload sequence!**"
    )

    # quote=False ensures it sends as a clean, standalone message
    await message.reply_text(
        text=welcome_text,
        quote=False
    )

# CHANGE THIS LINE
def register_handlers(app):
    app.add_handler(pyrogram.handlers.MessageHandler(start_handler, filters.command("start") & filters.private))
