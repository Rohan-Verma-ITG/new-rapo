from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings


class MongoConnection:
    client: AsyncIOMotorClient | None = None
    database: AsyncIOMotorDatabase | None = None


mongo = MongoConnection()


async def connect_to_mongo() -> None:
    mongo.client = AsyncIOMotorClient(settings.mongo_uri)
    mongo.database = mongo.client[settings.mongo_db_name]


async def close_mongo_connection() -> None:
    if mongo.client:
        mongo.client.close()


def get_db() -> AsyncIOMotorDatabase:
    if mongo.database is None:
        raise RuntimeError("MongoDB has not been initialized")
    return mongo.database
