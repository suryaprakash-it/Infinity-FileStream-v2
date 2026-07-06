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

    try:
        print("STEP 1 - Request received")

        file = await files.find_one({"_id": file_code})
        print("STEP 2 - MongoDB lookup done")

        if not file:
            return HTMLResponse(
                "<h2>❌ File Not Found</h2>",
                status_code=404
            )

        print("DATABASE:", file)

        print("STEP 3 - Calling get_messages()")

        msg = await bot.get_messages(
            chat_id=file["chat_id"],
            message_ids=file["message_id"]
        )

        print("STEP 4 - get_messages() completed")

        os.makedirs("downloads", exist_ok=True)

        print("STEP 5 - Starting download_media()")

        path = await bot.download_media(
            msg,
            file_name=f"downloads/{file['file_name']}"
        )

        print("STEP 6 - Download finished")
        print("PATH:", path)

        return FileResponse(
            path=path,
            filename=file["file_name"],
            media_type="application/octet-stream"
        )

    except Exception as e:
        import traceback

        print("========== ERROR ==========")
        traceback.print_exc()

        return HTMLResponse(
            f"<h2>{str(e)}</h2>",
            status_code=500
        )