from pyrogram import Client, filters
from datetime import datetime, timedelta
from config import Config
from helper.database import db
import asyncio
import time

# --- ADD PREMIUM COMMAND ---
@Client.on_message(filters.command("add_premium") & filters.user(Config.ADMIN_ID))
async def add_premium(client, message):
    try:
        # Command: /add_premium user_id days
        if len(message.command) != 3:
            return await message.reply_text("❌ **Usage:** `/add_premium user_id days`")
            
        user_id = int(message.command[1])
        days = int(message.command[2])
        
        new_expiry = datetime.now() + timedelta(days=days)
        await db.update_user(user_id, {"premium_expiry": new_expiry})
        
        await message.reply_text(f"✅ **Premium Added!**\nUser: `{user_id}`\nDuration: {days} days")
        
        # Notify the user
        try: await client.send_message(user_id, f"💎 **Congratulations!**\nYou are now a Premium Member for {days} days.")
        except: pass
        
    except Exception as e:
        await message.reply_text(f"Error: {e}")

# --- REMOVE PREMIUM COMMAND ---
@Client.on_message(filters.command("remove_premium") & filters.user(Config.ADMIN_ID))
async def remove_premium(client, message):
    try:
        if len(message.command) != 2:
            return await message.reply_text("❌ **Usage:** `/remove_premium user_id`")

        user_id = int(message.command[1])
        await db.update_user(user_id, {"premium_expiry": None})
        
        await message.reply_text("🚫 Premium Removed.")
        try: await client.send_message(user_id, "Your Premium Plan has been removed.")
        except: pass
        
    except Exception as e:
        await message.reply_text(f"Error: {e}")

# --- STATUS COMMAND ---
@Client.on_message(filters.command("status") & filters.user(Config.ADMIN_ID))
async def status_handler(client, message):
    users_count = await db.col.count_documents({})
    files_count = await db.files.count_documents({})
    await message.reply_text(f"📊 **BOT STATUS**\n\n👤 **Total Users:** {users_count}\n📂 **Total Files:** {files_count}")

# --- BROADCAST COMMAND ---
@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMIN_ID) & filters.reply)
async def broadcast_handler(client, message):
    msg = message.reply_to_message
    status_msg = await message.reply_text("📣 **Broadcast Started...**")
    
    total = await db.col.count_documents({})
    success = 0
    failed = 0
    start_time = time.time()
    
    async for user in db.col.find({}):
        try:
            await msg.copy(user['id'])
            success += 1
            await asyncio.sleep(0.1) # Prevent FloodWait
        except:
            failed += 1
            
    await status_msg.edit_text(
        f"✅ **Broadcast Completed**\n\n"
        f"👥 Total Users: {total}\n"
        f"✅ Success: {success}\n"
        f"❌ Failed: {failed}\n"
        f"⏱ Time Taken: {int(time.time() - start_time)}s"
    )