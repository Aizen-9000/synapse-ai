import os
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "synapse_ai")

# Initialize MongoDB client
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database(DB_NAME)

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