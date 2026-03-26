from datetime import datetime, timezone

import httpx
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import settings


class ShopifyService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def fetch_customer_profile(self, email: str) -> dict:
        if not settings.shopify_store_domain or not settings.shopify_admin_token:
            customer_snapshot = {"email": email, "note": "Shopify credentials not configured"}
            orders_snapshot = []
        else:
            base = f"https://{settings.shopify_store_domain}/admin/api/2024-10"
            headers = {"X-Shopify-Access-Token": settings.shopify_admin_token}
            async with httpx.AsyncClient(timeout=20) as client:
                customer_resp = await client.get(
                    f"{base}/customers/search.json", params={"query": f"email:{email}"}, headers=headers
                )
                customer_resp.raise_for_status()
                customers = customer_resp.json().get("customers", [])
                customer_snapshot = customers[0] if customers else {"email": email}

                orders_snapshot = []
                if customer_snapshot.get("id"):
                    orders_resp = await client.get(
                        f"{base}/orders.json",
                        params={
                            "customer_id": customer_snapshot["id"],
                            "limit": 10,
                            "status": "any",
                        },
                        headers=headers,
                    )
                    orders_resp.raise_for_status()
                    orders_snapshot = orders_resp.json().get("orders", [])

        synced_at = datetime.now(timezone.utc)
        await self.db.customers.update_one(
            {"email": email},
            {
                "$set": {
                    "email": email,
                    "customer_snapshot": customer_snapshot,
                    "orders_snapshot": orders_snapshot,
                    "synced_at": synced_at,
                }
            },
            upsert=True,
        )

        return {
            "email": email,
            "customer_snapshot": customer_snapshot,
            "orders_snapshot": orders_snapshot,
            "synced_at": synced_at,
        }
