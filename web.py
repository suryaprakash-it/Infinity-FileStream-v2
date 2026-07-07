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

    print("FILE PAGE:", file_code)

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

    print("DOWNLOAD START")

    try:
        file = await files.find_one({"_id": file_code})

        if not file:
            return {"error": "File not found"}

        print("DATABASE =", file)

        print("CHAT ID =", file["chat_id"])
        print("MESSAGE ID =", file["message_id"])

        chat = await bot.get_chat(file["chat_id"])
        print("CHAT =", chat)

        msg = await bot.get_messages(
            file["chat_id"],
            file["message_id"]
        )

        print("MESSAGE =", msg)

        media = (
            msg.document
            or msg.video
            or msg.audio
           