import motor.motor_asyncio
from config import Config
from datetime import datetime, timedelta

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.files = self.db.files

    async def add_user(self, id):
        if not await self.is_user_exist(id):
            user = {"id": int(id), "points": 0, "expiry": None, "premium_expiry": None}
            await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({"id": int(id)})
        return True if user else False

    async def get_user(self, id):
        return await self.col.find_one({"id": int(id)})

    async def update_user(self, id, data):
        await self.col.update_one({"id": int(id)}, {"$set": data})

    async def check_premium(self, id):
        user = await self.get_user(id)
        if not user: return False
        # Check Premium Date
        if user.get("premium_expiry") and user["premium_expiry"] > datetime.now(): return True
        # Check Temp Verification
        if user.get("expiry") and user["expiry"] > datetime.now(): return True
        return False

    async def add_file(self, file_info):
        # Prevent duplicates
        if not await self.files.find_one({"unique_id": file_info["unique_id"]}):
            await self.files.insert_one(file_info)

    async def search_files(self, query, offset=0):
        # Professional Regex Search
        filter_q = {"file_name": {"$regex": query, "$options": "i"}}
        cursor = self.files.find(filter_q)
        total = await self.files.count_documents(filter_q)
        results = await cursor.skip(offset).limit(10).to_list(10)
        return results, total

db = Database(Config.MONGO_URL, Config.DB_NAME)