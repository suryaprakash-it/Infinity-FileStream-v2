import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from telegram_client import bot
from handlers import register_handlers
from database import files
from config import Config

# --- SETUP ---
templates = Jinja2Templates(directory="templates")
download_semaphore = asyncio.Semaphore(2)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🤖 Starting Bot...")
    try:
        register_handlers(bot)
        await bot.start()

        # Inject private channel memory
        target_id = int(Config.STORAGE_CHAT_ID)
        access_hash = int(os.environ.get("CHANNEL_ACCESS_HASH", 0))
        if access_hash:
            await bot.storage.update_peers([(target_id, access_hash, "channel", None, None)])
            print("✅ Private Channel Memory Injected!")

        print("✅ Bot Started Successfully!")
    except Exception as e:
        print(f"❌ Critical Startup Error: {e}")
        raise e
    yield
    print("🛑 Stopping Bot...")
    await bot.stop()

app = FastAPI(title="Infinity FileStream", lifespan=lifespan)

@app.get("/")
async def home():
    return {"status": "online"}

@app.get("/file/{file_code}", response_class=HTMLResponse)
async def file_page(request: Request, file_code: str):
    file = await files.find_one({"_id": file_code})
    if not file:
        return HTMLResponse("<h2>❌ File Not Found</h2>", status_code=404)
    return templates.TemplateResponse("download.html", {
        "request": request,
        "file_name": file["file_name"],
        "file_size": file["file_size"],
        "file_code": file_code
    })

@app.get("/download/{file_code}")
async def download_file(request: Request, file_code: str):
    async with download_semaphore:
        try:
            file = await files.find_one({"_id": file_code})
            if not file:
                return {"error": "File not found"}

            msg = await bot.get_messages(int(file["chat_id"]), int(file["message_id"]))
            media = msg.document or msg.video or msg.audio or msg.photo
            if not media:
                return {"error": "No media found"}

            file_size = int(file["file_size"])
            range_header = request.headers.get("Range")

            # 1. Parse Range Header safely
            start, end = 0, file_size - 1
            status_code = 200

            if range_header:
                try:
                    parts = range_header.replace("bytes=", "").split("-")
                    start = int(parts[0]) if parts[0] else 0
                    end = int(parts[1]) if parts[1] and int(parts[1]) < file_size else file_size - 1
                    status_code = 206
                except Exception:
                    pass

            # 2. Safety Clamping
            start = max(0, start)
            end = min(end, file_size - 1)
            
            if start >= file_size:
                return {"error": "Invalid range"}

            chunk_size = (end - start) + 1

            # 3. Stream from Telegram
            async def file_stream():
                async for chunk in bot.stream_media(media, offset=start, limit=chunk_size):
                    yield chunk

            headers = {
                "Content-Disposition": f'attachment; filename="{file["file_name"]}"',
                "Accept-Ranges": "bytes",
                "Content-Type": "application/octet-stream"
            }

            if status_code == 206:
                headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"
            else:
                headers["Content-Length"] = str(file_size)

            return StreamingResponse(
                file_stream(),
                status_code=status_code,
                headers=headers
            )
        except Exception as e:
            print(f"Error in download: {e}")
            return {"error": "Download failed"}
