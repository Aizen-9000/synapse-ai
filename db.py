from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings


client = AsyncIOMotorClient(settings.MONGO_URI)
db = client.get_database(settings.DB_NAME)


# Collections
users_collection = db["users"]
chats_collection = db["chats"]
logs_collection = db["logs"]


# FastAPI dependency helpers
async def get_users_collection():
    yield users_collection


async def get_chats_collection():
    yield chats_collection


async def get_logs_collection():
    yield logs_collection