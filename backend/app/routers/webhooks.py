import json

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.middleware.security import SecurityService
from app.services.dependencies import get_database
from app.services.shopify_service import ShopifyService
from app.services.webhook_service import WebhookService

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/orders/create")
async def webhook_orders_create(
    request: Request,
    x_shopify_hmac_sha256: str = Header(default=""),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    body = await request.body()
    if not SecurityService.verify_shopify_hmac(body, x_shopify_hmac_sha256):
        raise HTTPException(status_code=401, detail="Invalid Shopify HMAC")
    payload = json.loads(body.decode("utf-8"))
    email = payload.get("email") or payload.get("customer", {}).get("email")
    if email:
        await ShopifyService(db).fetch_customer_profile(email)
    return {"ok": True}


@router.post("/customers/update")
async def webhook_customers_update(
    request: Request,
    x_shopify_hmac_sha256: str = Header(default=""),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    body = await request.body()
    if not SecurityService.verify_shopify_hmac(body, x_shopify_hmac_sha256):
        raise HTTPException(status_code=401, detail="Invalid Shopify HMAC")
    payload = json.loads(body.decode("utf-8"))
    email = payload.get("email")
    if email:
        await ShopifyService(db).fetch_customer_profile(email)
    return {"ok": True}


@router.post("/email/inbound")
async def webhook_email_inbound(request: Request, db: AsyncIOMotorDatabase = Depends(get_database)):
    form = await request.form()
    timestamp = str(form.get("timestamp", ""))
    token = str(form.get("token", ""))
    signature = str(form.get("signature", ""))

    if not SecurityService.verify_mailgun_signature(timestamp, token, signature):
        raise HTTPException(status_code=401, detail="Invalid Mailgun signature")

    sender = str(form.get("sender", "")).split("<")[-1].replace(">", "")
    subject = str(form.get("subject", "No subject"))
    body_plain = str(form.get("body-plain", ""))

    message = await WebhookService(db).process_inbound_email(sender, subject, body_plain)
    return {"ok": True, "message_id": message["_id"]}
