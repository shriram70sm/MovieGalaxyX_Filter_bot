import os

class Config:
    # --- API TOKENS ---
    API_ID = 12345678  # Replace with your API_ID
    API_HASH = "your_api_hash_here"
    BOT_TOKEN = "your_bot_token_here"
    
    # --- DATABASE ---
    MONGO_URL = "mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority"
    DB_NAME = "MovieGalaxyX"
    
    # --- CHANNELS ---
    ADMIN_ID = 123456789             # Your Telegram ID
    FILES_CHANNEL = -1001234567890   # Channel where you upload files
    BACKUP_CHANNEL = -1009876543210  # Backup Channel (0 to disable)
    LOG_CHANNEL = -1005555555555     # Logs Channel (0 to disable)

    # --- FORCE SUBSCRIBE ---
    # Users must join these channels to use the bot
    FS_CHANNELS = [-1001111111111] 
    FS_LINKS = ["https://t.me/YourChannelLink"]

    # --- MONETIZATION (Shortener Rotation) ---
    # The bot picks a random one to prevent bypassing
    SHORTENERS = [
        {"api": "api_key_1", "url": "https://gplinks.in/api"},
        {"api": "api_key_2", "url": "https://yorurl.com/api"},
        # Add more if needed
    ]
    
    VERIFY_TIME = 1800 # 30 Minutes (in seconds)
    REFER_POINTS = 10  # Points per invite
    
    # --- PAYMENT (Premium) ---
    UPI_ID = "your_upi@okaxis"
    UPI_QR = "https://graph.org/file/your_qr_code.jpg" # Upload your QR to telegraph
    PREMIUM_PRICE = "₹50/1Week,\n₹100/1Month,\n₹250/3Months"

    # --- IMAGES ---
    PICS = [
        "https://graph.org/file/961858025257545931758.jpg",
        "https://telegra.ph/file/p/8d/6f2e374528345723467.jpg"
    ]