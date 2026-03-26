import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.middleware.security import SecurityService


async def main():
    client = AsyncIOMotorClient(settings.mongo_uri)
    db = client[settings.mongo_db_name]

    await db.agents.update_one(
        {"email": "agent@demo.com"},
        {
            "$set": {
                "email": "agent@demo.com",
                "name": "Demo Agent",
                "role": "admin",
                "password_hash": SecurityService.hash_password("Password123!"),
            }
        },
        upsert=True,
    )

    await db.automation_rules.update_one(
        {"name": "Refund Router"},
        {
            "$set": {
                "name": "Refund Router",
                "trigger": "message.received",
                "conditions": {"keyword": "refund"},
                "actions": {"add_tag": "refund", "send_ai_reply": True},
                "enabled": True,
            }
        },
        upsert=True,
    )

    client.close()
    print("Seed completed")


if __name__ == "__main__":
    asyncio.run(main())
