from contextlib import asynccontextmanager

from fastapi import FastAPI
from telegram_client import bot
from handlers import register_handlers


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
    title="Infinity FileStream v2",
    lifespan=lifespan
)


@app.get("/")
async def home():
    return {
        "status": "online",
        "bot": "Infinity FileStream v2"
    }