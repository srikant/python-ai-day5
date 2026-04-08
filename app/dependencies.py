from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:secret@localhost:27017")
DB_NAME = os.getenv("DB_NAME", "alerts_db")

_client: AsyncIOMotorClient | None = None

def get_mongo_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(MONGO_URI)
    return _client

async def get_database() -> AsyncIOMotorDatabase:
    client = get_mongo_client()
    return client[DB_NAME]