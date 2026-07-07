import os
import asyncio # Add this import
from contextlib import asynccontextmanager
# ... (Keep your existing imports)

# ADD THIS LINE: Only allow 2 simultaneous downloads at once
# This prevents the "Server error" and stops the connection overload
download_semaphore = asyncio.Semaphore(2) 

# ... (Keep lifespan and app definition)

@app.get("/download/{file_code}")
async def download_file(request: Request, file_code: str):
    # USE THE BOUNCER
    async with download_semaphore:
        try:
            file = await files.find_one({"_id": file_code})
            if not file:
                return {"error": "File not found"}

            msg = await bot.get_messages(int(file["chat_id"]), int(file["message_id"]))
            
            # ... (Rest of your existing logic stays exactly the same)
            
            # Streaming part:
            async def file_stream():
                async for chunk in bot.stream_media(media, offset=start, limit=chunk_size):
                    yield chunk

            return StreamingResponse(
                file_stream(),
                status_code=status_code,
                media_type="application/octet-stream",
                headers=headers
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"error": str(e)}
