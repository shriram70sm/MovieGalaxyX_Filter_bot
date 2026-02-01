# 🎬 MovieGalaxyX - Ultimate Auto Filter Bot

<p align="center">
  <img src="https://i.postimg.cc/5t7zQWng/Filter_logo.jpg" alt="MovieGalaxyX Bot">
</p>

<p align="center">
  <b>A Professional, Modular, and Monetized Auto-Filter Bot for Telegram.</b><br>
  Built with Pyrogram & MongoDB.
</p>

---

## 🔥 Key Features

* **⚡ Smart Search UI:** Filter results by **Language**, **Quality**, and **Season** with interactive buttons.
* **💸 Monetization Ready:**
    * **Shortener Rotation:** Randomly rotates between multiple shorteners to prevent bypassing.
    * **Premium System:** UPI/QR Code payment support with Admin verification.
* **🛡️ Verification System:** Forces free users to verify via ad-links every 30 minutes.
* **♻️ Auto-Delete:** Automatically deletes sent files after **10 Minutes** to protect your channel.
* **📂 Auto-Backup:** Copies every file uploaded to the main channel into a private backup channel.
* **📢 Admin Dashboard:** Broadcast messages, check status, and manage premium users.
* **🔐 Force Subscribe:** Compels users to join your Updates Channel.
* **📄 Pagination:** Smooth "Next/Previous" navigation for thousands of files.

---

## 🛠️ Config Variables

You need to fill these variables in `config.py`:

| Variable | Description |
| :--- | :--- |
| `API_ID` | Get this from my.telegram.org |
| `API_HASH` | Get this from my.telegram.org |
| `BOT_TOKEN` | Get this from @BotFather |
| `MONGO_URL` | Your MongoDB Atlas Connection String |
| `ADMIN_ID` | Your Telegram User ID (for Admin commands) |
| `FILES_CHANNEL` | Channel ID where you upload files (e.g., -100xxxx) |
| `BACKUP_CHANNEL` | Channel ID for file backup (Optional) |
| `LOG_CHANNEL` | Channel ID for User Logs (Optional) |
| `FS_CHANNELS` | List of Channel IDs for Force Subscribe |
| `SHORTENERS` | List of Shortener APIs (API Key & URL) |
| `UPI_ID` | Your UPI ID for Premium Payments |
| `UPI_QR` | Direct link to your QR Code image |

---

## 🤖 Admin Commands

| Command | Usage |
| :--- | :--- |
| `/start` | Check if bot is alive |
| `/status` | See Total Users & Files indexed |
| `/broadcast` | Reply to a message to send it to all users |
| `/add_premium` | `/add_premium user_id days` (e.g., `/add_premium 123456 30`) |
| `/remove_premium`| `/remove_premium user_id` |

---

## 🚀 How to Deploy

### Method 1: Heroku
1. Fork this repository.
2. Go to Heroku Dashboard > New App.
3. Connect GitHub > Select this Repo.
4. Click **Deploy Branch**.
5. (Optional) Add Environment Variables in Settings if you use `os.environ`.

### Method 2: Koyeb / Render
1. Connect your GitHub Repository.
2. **Build Command:** `pip install -r requirements.txt`
3. **Run Command:** `python bot.py`

### Method 3: Local / VPS
```bash
git clone [https://github.com/YourUsername/MovieGalaxyX.git](https://github.com/YourUsername/MovieGalaxyX.git)
cd MovieGalaxyX
pip3 install -r requirements.txt
python3 bot.py
