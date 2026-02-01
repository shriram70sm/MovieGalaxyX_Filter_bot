from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config

class Script:
    START_TXT = """
**👋 Hello {}**

✨ **I AM A POWERFUL AUTO-FILTER BOT.**
✨ **I provide Movies & Series in all Qualities.**
✨ **Add me to your group & make me Admin.**

©️ **Maintained By MovieGalaxyX**
"""

    HELP_TXT = """
**ℹ️ HELP MENU**

1. **Search:** Type any movie name (e.g., "Avengers").
2. **Filter:** Click buttons like '1080p' or 'Hindi' to refine results.
3. **Verify:** If asked, verify to get free access.
"""

    ABOUT_TXT = "🤖 **Name:** MovieGalaxyX\n⚡ **Server:** High Speed\n🐍 **Language:** Python 3"

    PREMIUM_TXT = f"""
💎 **PREMIUM SUBSCRIPTION**

✅ **No Ads / Shorteners**
✅ **Direct File Access**
✅ **High Speed Download**
✅ **Priority Support**

💰 **Price:** {Config.PREMIUM_PRICE}

**1. Pay to UPI:** `{Config.UPI_ID}`
**2. Or Scan the QR Code above.**
**3. Send Screenshot to Admin.**

👤 **Admin:** [Click Here](tg://user?id={Config.ADMIN_ID})
"""

    @staticmethod
    def start_buttons(bot_username, user_id):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Me To Your Group ➕", url=f"https://t.me/{bot_username}?startgroup=true")],
            # REFERRAL BUTTON REMOVED HERE
            [InlineKeyboardButton("🔄 UPDATES CHANNEL", url=Config.FS_LINKS[0] if Config.FS_LINKS else "https://t.me/MovieGalaxyX_Link")],
            [InlineKeyboardButton("ℹ️ HELP", callback_data="help"), InlineKeyboardButton("🤖 ABOUT", callback_data="about")],
            [InlineKeyboardButton("💎 UNLOCK PREMIUM 💎", callback_data="premium")],
            [InlineKeyboardButton("®️ MY PLAN", callback_data="my_plan")]
        ])

    @staticmethod
    def filter_buttons(query):
        return [
            [
                InlineKeyboardButton("🗣 LANGUAGES", callback_data=f"lang_{query}"),
                InlineKeyboardButton("📺 QUALITIES", callback_data=f"qual_{query}"),
                InlineKeyboardButton("📅 SEASONS", callback_data=f"season_{query}")
            ],
            [InlineKeyboardButton("⭕ HOW TO DOWNLOAD ⭕", url="https://t.me/MovieGalaxyX_Link")]
        ]