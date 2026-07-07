from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from telegram_client import bot
from handlers import register_handlers
from database import files
from config import Config

# Initialize templates
templates = Jinja2Templates(directory="templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🤖 Starting Bot...")
    try:
        register_handlers(bot)
        await bot.start()
        
        # Ensure STORAGE_CHAT_ID is an integer for Pyrogram resolution
        storage_id = int(Config.STORAGE_CHAT_ID)
        
        # Warm up the session to prevent 'Peer id invalid' errors
        chat = await bot.get_chat(storage_id)
        print(f"✅ Successfully resolved storage channel: {chat.title}")
        
        print("✅ Bot Started Successfully!")
    except Exception as e:
        print(f"❌ Critical Startup Error: {e}")
        raise e

    yield

    print("🛑 Stopping Bot...")
    await bot.stop()
    print("✅ Bot Stopped.")

app = FastAPI(
    title="Infinity FileStream",
    lifespan=lifespan
)

@app.get("/")
async def home():
    return {"status": "online"}

@app.get("/file/{file_code}", response_class=HTMLResponse)
async def file_page(request: Request, file_code: str):
    file = await files.find_one({"_id": file_code})

    if not file:
        return HTMLResponse("<h2>❌ File Not Found</h2>", status_code=404)

    return templates.TemplateResponse(
        "download.html",
        {
            "request": request,
            "file_name": file["file_name"],
            "file_size": file["file_size"],
            "file_code": file_code
        }
    )

@app.get("/download/{file_code}")
async def download_file(file_code: str):
    try:
        file = await files.find_one({"_id": file_code})
        if not file:
            return {"error": "File not found"}

        # Fetch the message from storage channel
        msg = await bot.get_messages(file["chat_id"], file["message_id"])
        
        # Determine media type
        media = msg.document or msg.video or msg.audio or msg.photo
        if not media:
            return {"error": "No media found in message"}

        # Stream directly from Telegram
        async def file_stream():
            async for chunk in bot.stream_media(media):
                yield chunk

        return StreamingResponse(
            file_stream(),
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f'attachment; filename="{file["file_name"]}"',
                "Content-Length": str(file["file_size"])
            }
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
