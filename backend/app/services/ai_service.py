import json

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from openai import AsyncOpenAI

from app.core.config import settings


class AIService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    async def suggest_reply(self, ticket_id: str) -> dict:
        ticket = await self.db.tickets.find_one({"_id": ObjectId(ticket_id)})
        if not ticket:
            raise ValueError("Ticket not found")

        last_message = await self.db.messages.find_one({"ticket_id": ticket_id}, sort=[("created_at", -1)])
        customer = await self.db.customers.find_one({"email": ticket["customer_email"]})

        customer_data = customer.get("customer_snapshot", {}) if customer else {}
        orders = customer.get("orders_snapshot", []) if customer else []

        if not self.client:
            return {
                "intent": "order_status",
                "confidence": 0.51,
                "suggested_reply": "Thanks for contacting us. We are reviewing your order and will update you shortly.",
            }

        prompt = {
            "ticket_subject": ticket.get("subject"),
            "customer": customer_data,
            "orders": orders[:10],
            "last_message": (last_message or {}).get("body", ""),
            "constraints": ["under 150 words", "factual", "no hallucinations"],
            "allowed_intents": ["order_status", "refund", "cancel"],
        }

        response = await self.client.responses.create(
            model=settings.openai_model,
            input=[
                {
                    "role": "system",
                    "content": "You are a Shopify support copilot. Respond in JSON: intent, confidence, suggested_reply.",
                },
                {"role": "user", "content": json.dumps(prompt)},
            ],
            temperature=0.2,
        )
        parsed = json.loads(response.output_text)
        return {
            "intent": parsed.get("intent", "order_status"),
            "confidence": float(parsed.get("confidence", 0.5)),
            "suggested_reply": parsed.get("suggested_reply", ""),
        }
