from motor.motor_asyncio import AsyncIOMotorDatabase

from app.services.utils import to_object_id


class AutomationService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def run(self, trigger: str, ticket: dict, message: dict | None = None) -> list[dict]:
        actions_applied: list[dict] = []
        cursor = self.db.automation_rules.find({"trigger": trigger, "enabled": True})

        async for rule in cursor:
            conditions = rule.get("conditions", {})
            keyword = conditions.get("keyword")
            message_body = (message or {}).get("body", "").lower()

            if keyword and keyword.lower() not in message_body:
                continue

            actions = rule.get("actions", {})
            updates = {}
            if assign_agent := actions.get("assign_agent"):
                updates["assignee_id"] = assign_agent
                actions_applied.append({"type": "assign_agent", "value": assign_agent})

            if add_tag := actions.get("add_tag"):
                tags = set(ticket.get("tags", []))
                tags.add(add_tag)
                updates["tags"] = list(tags)
                actions_applied.append({"type": "add_tag", "value": add_tag})

            if updates:
                await self.db.tickets.update_one({"_id": to_object_id(str(ticket["_id"]))}, {"$set": updates})

            if actions.get("send_ai_reply"):
                actions_applied.append({"type": "send_ai_reply", "value": True})

        return actions_applied
