from datetime import timedelta

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.services.activity_service import ActivityService
from app.services.automation_service import AutomationService
from app.services.utils import normalize_doc, now_utc, to_object_id


class TicketService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.activity = ActivityService(db)
        self.automation = AutomationService(db)

    async def create_ticket(self, payload: dict, source: str, actor: str) -> dict:
        created_at = now_utc()
        doc = {
            **payload,
            "source": source,
            "assignee_id": payload.get("assignee_id"),
            "sla_due_at": created_at + timedelta(hours=24),
            "created_at": created_at,
            "updated_at": created_at,
        }
        result = await self.db.tickets.insert_one(doc)
        ticket = await self.db.tickets.find_one({"_id": result.inserted_id})
        await self.activity.log(str(result.inserted_id), "ticket.created", actor, {"source": source})
        await self.automation.run("ticket.created", ticket)
        return normalize_doc(ticket)

    async def list_tickets(self, filters: dict) -> list[dict]:
        query = {k: v for k, v in filters.items() if v}
        cursor = self.db.tickets.find(query).sort("updated_at", -1)
        return [normalize_doc(ticket) async for ticket in cursor]

    async def get_ticket(self, ticket_id: str) -> dict | None:
        ticket = await self.db.tickets.find_one({"_id": to_object_id(ticket_id)})
        return normalize_doc(ticket) if ticket else None

    async def patch_ticket(self, ticket_id: str, updates: dict, actor: str) -> dict | None:
        updates = {k: v for k, v in updates.items() if v is not None}
        if not updates:
            return await self.get_ticket(ticket_id)

        updates["updated_at"] = now_utc()
        await self.db.tickets.update_one({"_id": to_object_id(ticket_id)}, {"$set": updates})
        await self.activity.log(ticket_id, "ticket.updated", actor, updates)
        return await self.get_ticket(ticket_id)

    async def append_message(self, ticket_id: str, payload: dict, actor: str) -> dict:
        doc = {**payload, "ticket_id": ticket_id, "created_at": now_utc()}
        result = await self.db.messages.insert_one(doc)
        await self.db.tickets.update_one(
            {"_id": to_object_id(ticket_id)}, {"$set": {"updated_at": now_utc(), "status": "pending"}}
        )
        inserted = await self.db.messages.find_one({"_id": result.inserted_id})
        await self.activity.log(ticket_id, "message.sent", actor, {"sender": payload["sender_email"]})
        ticket = await self.db.tickets.find_one({"_id": to_object_id(ticket_id)})
        await self.automation.run("message.received", ticket, inserted)
        return normalize_doc(inserted)

    async def list_messages(self, ticket_id: str) -> list[dict]:
        cursor = self.db.messages.find({"ticket_id": ticket_id}).sort("created_at", 1)
        return [normalize_doc(message) async for message in cursor]
