import secrets
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from helper.database import db
from helper.utils import get_shortlink, get_missing_channels

@Client.on_message(filters.text & filters.private & ~filters.command(["start", "broadcast", "status"]))
async def search_handler(client, message):
    user_id = message.from_user.id
    query = message.text

    # 1. Force Subscribe Check
    missing = await get_missing_channels(client, user_id)
    if missing:
        btns = [[InlineKeyboardButton(f"📢 Join Channel {i+1}", url=Config.FS_LINKS[i])] for i in missing]
        btns.append([InlineKeyboardButton("🔄 Try Again", callback_data="check_sub")])
        await message.reply_text("⚠️ **Please Join Our Channels First!**", reply_markup=InlineKeyboardMarkup(btns))
        return

    # 2. Access/Verification Check
    if Config.SHORTENERS and not await db.check_premium(user_id):
        token = secrets.token_urlsafe(8)
        await db.update_user(user_id, {"verify_token": token})
        link = await get_shortlink(f"https://t.me/{client.me.username}?start=verify_{token}")
        
        btn = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 Verify Now", url=link)],
            [InlineKeyboardButton("💎 Buy Premium", callback_data="premium")]
        ])
        await message.reply_text("⚠️ **Free Access Expired!**\nVerify to get 30 mins access or Buy Premium.", reply_markup=btn)
        return

    # 3. Perform Search
    results, total = await db.search_files(query, 0)
    
    if not results:
        await message.reply_text("❌ **No results found.**\nTry searching with a simpler name.")
        return

    # 4. Build Professional Result Buttons
    buttons = []
    for file in results:
        # Format: [1.2GB] Movie Name
        buttons.append([InlineKeyboardButton(f"📁 {file['file_name']}", callback_data=f"file_{file['unique_id']}")])

    # 5. Smart Filter Buttons
    buttons.append([
        InlineKeyboardButton("🗣 LANGUAGE", callback_data=f"lang_{query}"),
        InlineKeyboardButton("📺 QUALITY", callback_data=f"qual_{query}"),
        InlineKeyboardButton("📅 SEASON", callback_data=f"season_{query}")
    ])
    buttons.append([InlineKeyboardButton("⭕ HOW TO DOWNLOAD ⭕", url="https://t.me/MovieGalaxyX_Link")])

    # 6. Pagination
    if total > 10:
        buttons.append([
            InlineKeyboardButton("📄 1", callback_data="pages"),
            InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{query}_10")
        ])

    await message.reply_text(f"🔎 **Results for:** `{query}`", reply_markup=InlineKeyboardMarkup(buttons))