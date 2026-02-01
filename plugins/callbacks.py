import asyncio
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from config import Config
from helper.database import db
from helper.utils import auto_delete, PREMIUM_TXT, START_TXT, get_missing_channels
from script import Script

@Client.on_callback_query()
async def cb_handler(client, cb):
    data = cb.data
    user_id = cb.from_user.id

    if data == "check_sub":
        if not await get_missing_channels(client, user_id):
            await cb.message.delete()
            await cb.message.reply_text("✅ **Joined!** You can search now.")
        else:
            await cb.answer("❌ You are still not in the channel!", show_alert=True)
        return

    # --- Start Menu Callbacks ---
    if data == "start":
        if Config.PICS:
            await cb.message.edit_media(
                InputMediaPhoto(Config.PICS[0], caption=START_TXT.format(cb.from_user.first_name)), 
                reply_markup=Script.start_buttons(client.me.username, user_id)
            )
        else:
            await cb.message.edit_text(
                START_TXT.format(cb.from_user.first_name),
                reply_markup=Script.start_buttons(client.me.username, user_id)
            )

    elif data == "help":
         await cb.message.edit_caption(Script.HELP_TXT, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]]))

    elif data == "about":
         await cb.message.edit_caption(Script.ABOUT_TXT, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]]))

    elif data == "premium":
        if Config.UPI_QR:
            await cb.message.edit_media(InputMediaPhoto(Config.UPI_QR, caption=PREMIUM_TXT),
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]]))
        else:
            await cb.message.edit_caption(PREMIUM_TXT, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]]))

    elif data == "my_plan":
        is_prem = await db.check_premium(user_id)
        status = "💎 PREMIUM" if is_prem else "👤 FREE"
        await cb.message.edit_caption(f"📊 **Plan:** {status}", 
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="start")]]))

    # --- FILTER LOGIC ---
    elif data.startswith(("lang_", "qual_", "season_")):
        _, query = data.split("_", 1)
        if data.startswith("lang_"):
            opts = ["Hindi", "English", "Tamil", "Telugu", "Malayalam", "Dual", "Multi"]
        elif data.startswith("qual_"):
            opts = ["480p", "720p", "1080p", "2160p", "4k", "HD", "CAM"]
        else:
            opts = [f"S{i:02d}" for i in range(1, 11)]
        
        btns = []
        for opt in opts:
            btns.append(InlineKeyboardButton(opt, callback_data=f"refine_{query} {opt}"))
        
        grid = [btns[i:i+3] for i in range(0, len(btns), 3)]
        grid.append([InlineKeyboardButton("🔙 Back", callback_data=f"back_{query}")])
        
        await cb.message.edit_text(f"👇 **Select Option for:** `{query}`", reply_markup=InlineKeyboardMarkup(grid))

    # --- REFINED SEARCH ---
    elif data.startswith("refine_"):
        new_query = data.split("_", 1)[1]
        results, total = await db.search_files(new_query, 0)
        
        if not results:
            await cb.answer("No files found with that filter!", show_alert=True)
            return

        btns = [[InlineKeyboardButton(f"📁 {f['file_name']}", callback_data=f"file_{f['unique_id']}")] for f in results]
        
        btns.append([
            InlineKeyboardButton("🗣 LANG", callback_data=f"lang_{new_query}"),
            InlineKeyboardButton("📺 QUAL", callback_data=f"qual_{new_query}"),
            InlineKeyboardButton("📅 SEASON", callback_data=f"season_{new_query}")
        ])

        if total > 10:
             btns.append([InlineKeyboardButton("📄 1", callback_data="p"), InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{new_query}_10")])
        
        await cb.message.edit_text(f"🔎 **Filtered:** `{new_query}`", reply_markup=InlineKeyboardMarkup(btns))

    # --- PAGINATION ---
    elif data.startswith(("next_", "prev_", "back_")):
        if data.startswith("back_"):
            query = data.split("_", 1)[1]; offset = 0
        else:
            _, query, offset = data.split("_", 2)
            offset = int(offset)

        results, total = await db.search_files(query, offset)
        btns = [[InlineKeyboardButton(f"📁 {f['file_name']}", callback_data=f"file_{f['unique_id']}")] for f in results]
        
        btns.append([
            InlineKeyboardButton("🗣 LANG", callback_data=f"lang_{query}"),
            InlineKeyboardButton("📺 QUAL", callback_data=f"qual_{query}"),
            InlineKeyboardButton("📅 SEASON", callback_data=f"season_{query}")
        ])

        nav = []
        if offset >= 10: nav.append(InlineKeyboardButton("⏪ PREV", callback_data=f"prev_{query}_{offset-10}"))
        nav.append(InlineKeyboardButton(f"📄 {int(offset/10)+1}", callback_data="pages"))
        if offset + 10 < total: nav.append(InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{query}_{offset+10}"))
        btns.append(nav)

        await cb.message.edit_text(f"🔎 **Results for:** `{query}`", reply_markup=InlineKeyboardMarkup(btns))

    # --- SEND FILE (With Branding) ---
    elif data.startswith("file_"):
        uid = data.split("_")[1]
        file = await db.files.find_one({"unique_id": uid})
        if file:
            await cb.answer("Sending...")
            btn = InlineKeyboardMarkup([[
                InlineKeyboardButton("🚀 FAST DOWNLOAD / WATCH ONLINE 🖥️", url=f"https://t.me/{client.me.username}"),
                InlineKeyboardButton("❌ CLOSE ❌", callback_data="close")
            ]])
            
            caption = (
                f"🎥 **{file['file_name']}**\n\n"
                f"⚠️ __Auto-deletes in 10 mins!__\n\n"
                f"🤖 **Download via:** @{client.me.username}" 
            )

            msg = await cb.message.reply_cached_media(
                file['file_id'], 
                caption=caption, 
                reply_markup=btn
            )
            asyncio.create_task(auto_delete(msg))
            
            if Config.BACKUP_CHANNEL:
                try: await client.send_cached_media(Config.BACKUP_CHANNEL, file['file_id'], caption=file['file_name'])
                except: pass
        else:
            await cb.answer("File not found in DB!", show_alert=True)

    elif data == "close":
        await cb.message.delete()