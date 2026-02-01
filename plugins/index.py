from pyrogram import Client, filters
from config import Config
from helper.database import db

@Client.on_message(filters.chat(Config.FILES_CHANNEL) & (filters.document | filters.video))
async def index_files(client, message):
    media = message.document or message.video
    if not media: return
    
    file_info = {
        "unique_id": media.file_unique_id,
        "file_id": media.file_id,
        "file_name": media.file_name or message.caption or "Unknown File",
        "file_size": media.file_size,
        "caption": message.caption,
        "message_id": message.id
    }
    
    # Save to DB
    await db.add_file(file_info)
    print(f"✅ Indexed: {file_info['file_name']}")

    # Auto-Backup
    if Config.BACKUP_CHANNEL:
        try: await message.copy(Config.BACKUP_CHANNEL)
        except Exception as e: print(f"Backup Error: {e}")