from motor.motor_asyncio import AsyncIOMotorDatabase

from app.services.utils import now_utc


class ActivityService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def log(self, ticket_id: str, event_type: str, actor: str, payload: dict | None = None):
        await self.db.activity_logs.insert_one(
            {
                "ticket_id": ticket_id,
                "event_type": event_type,
                "actor": actor,
                "payload": payload or {},
                "created_at": now_utc(),
            }
        )
