from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.enums import TicketPriority, TicketStatus
from app.services.ticket_service import TicketService


class WebhookService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.ticket_service = TicketService(db)

    async def process_inbound_email(self, sender: str, subject: str, body: str):
        ticket = await self.db.tickets.find_one({"subject": subject, "customer_email": sender})
        if not ticket:
            created = await self.ticket_service.create_ticket(
                {
                    "subject": subject,
                    "customer_email": sender,
                    "status": TicketStatus.open,
                    "priority": TicketPriority.medium,
                    "tags": ["email"],
                },
                source="email",
                actor="mailgun",
            )
            ticket_id = created["_id"]
        else:
            ticket_id = str(ticket["_id"])

        return await self.ticket_service.append_message(
            ticket_id,
            {
                "body": body,
                "sender_type": "customer",
                "sender_email": sender,
                "is_internal": False,
            },
            actor="mailgun",
        )
