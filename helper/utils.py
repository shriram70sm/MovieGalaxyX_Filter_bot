import aiohttp
import random
import asyncio
from config import Config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

async def get_shortlink(url):
    if not Config.SHORTENERS: return url
    site = random.choice(Config.SHORTENERS)
    try:
        params = {'api': site['api'], 'url': url}
        async with aiohttp.ClientSession() as session:
            async with session.get(site['url'], params=params) as resp:
                data = await resp.json()
                return data.get("shortenedUrl") or data.get("short_url") or url
    except Exception as e:
        print(f"Shortener Error: {e}")
        return url

async def auto_delete(message, time=600):
    await asyncio.sleep(time)
    try: await message.delete()
    except: pass

async def get_missing_channels(client, user_id):
    missing = []
    for index, channel_id in enumerate(Config.FS_CHANNELS):
        if not channel_id: continue
        try:
            user = await client.get_chat_member(channel_id, user_id)
            if user.status in ["left", "kicked", "banned"]: missing.append(index)
        except UserNotParticipant:
            missing.append(index)
        except Exception:
            missing.append(index) # Assume missing if error
    return missing

# --- TEXT TEMPLATES ---
START_TXT = """
**👋 Hello {}**

✨ **I AM A POWERFUL AUTO-FILTER BOT.**
✨ **I provide Movies & Series in all Qualities.**
✨ **Add me to your group & make me Admin.**

©️ **Maintained By Owner**
"""

PREMIUM_TXT = f"""
💎 **PREMIUM SUBSCRIPTION**

✅ **No Ads / Shorteners**
✅ **Direct File Access**
✅ **High Speed Download**

💰 **Price:** {Config.PREMIUM_PRICE}

**1. Pay to UPI:** `{Config.UPI_ID}`
**2. Or Scan the QR Code.**
**3. Send Screenshot to Admin.**

👤 **Admin:** [Click Here](tg://user?id={Config.ADMIN_ID})
"""