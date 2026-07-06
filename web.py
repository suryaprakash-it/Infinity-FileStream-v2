from contextlib import asynccontextmanager
import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from telegram_client import bot
from handlers import register_handlers
from database import files

templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🤖 Starting Bot...")

    register_handlers(bot)

    await bot.start()

    print("✅ Bot Started!")

    yield

    print("🛑 Stopping Bot...")

    await bot.stop()


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
        return HTMLResponse(
            "<h2>❌ File Not Found</h2>",
            status_code=404
        )

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
            return HTMLResponse(
                "<h2>❌ File Not Found</h2>",
                status_code=404
            )

        print("========== DOWNLOAD START ==========")
        print("DATABASE:", file)

        msg = await bot.get_messages(
            file["chat_id"],
            file["message_id"]
        )

        print("MESSAGE:", msg)

        os.makedirs("downloads", exist_ok=True)

        path = await bot.download_media(
            msg,
            file_name=f"downloads/{file['file_name']}"
        )

        print("DOWNLOADED TO:", path)
        print("========== DOWNLOAD END ==========")

        return FileResponse(
            path=path,
            filename=file["file_name"],
            media_type="application/octet-stream"
        )

    except Exception as e:
        print("========== DOWNLOAD ERROR ==========")
        print(e)
        import traceback
        traceback.print_exc()

        return HTMLResponse(
            f"<h2>Download Error</h2><pre>{e}</pre>",
            status_code=500
        )