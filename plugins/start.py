import secrets
import random
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from helper.database import db
from helper.utils import START_TXT
from script import Script

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = message.from_user.id
    text = message.text.split()
    
    # 1. Add User (Removed Referral Logic)
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id)
        
        # Log New User
        if Config.LOG_CHANNEL:
            try:
                log_msg = (
                    f"#NEW_USER\n\n"
                    f"👤 **User:** {message.from_user.mention}\n"
                    f"🆔 **ID:** `{user_id}`\n"
                    f"📅 **Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
                await client.send_message(Config.LOG_CHANNEL, log_msg)
            except Exception: pass

    # 2. Check Verification Payload
    if len(text) > 1 and text[1].startswith("verify_"):
        token = text[1].split("_")[1]
        user = await db.get_user(user_id)
        if user and user.get("verify_token") == token:
            new_expiry = datetime.now() + timedelta(seconds=Config.VERIFY_TIME)
            await db.update_user(user_id, {"expiry": new_expiry, "verify_token": None})
            await message.reply_text("✅ **Verified Successfully! You can now search.**")
            return
        else:
            await message.reply_text("❌ **Invalid or Expired Link.**")
            return

    # 3. Send Start Message
    if Config.PICS:
        await message.reply_photo(
            photo=random.choice(Config.PICS),
            caption=START_TXT.format(message.from_user.first_name),
            reply_markup=Script.start_buttons(client.me.username, user_id)
        )
    else:
        await message.reply_text(
            text=START_TXT.format(message.from_user.first_name),
            reply_markup=Script.start_buttons(client.me.username, user_id),
            disable_web_page_preview=True
        )