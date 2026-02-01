from pyrogram import Client
from aiohttp import web
from config import Config
from helper.database import db
from route import web_server # Import the web server
import asyncio
import logging

# Setup Logger
logging.basicConfig(level=logging.INFO)

class Bot(Client):
    def __init__(self):
        super().__init__(
            "MyProBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="plugins")
        )

    async def start(self):
        await super().start()
        print("🔥 Bot Started!")
        
        # 1. Create Database Index (Speed Boost)
        await db.files.create_index([("file_name", "text")])

        # 2. Send Alert to Log Channel
        if Config.LOG_CHANNEL:
            try: 
                await self.send_message(Config.LOG_CHANNEL, "🤖 **Bot has restarted and is Online!**")
            except Exception as e:
                print(f"Log Channel Error: {e}")

        # 3. Start Web Server (Keep Alive)
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", 8080).start()
        print("✅ Web Server Started on Port 8080")

    async def stop(self, *args):
        await super().stop()
        print("🔴 Bot Stopped")

if __name__ == "__main__":
    Bot().run()