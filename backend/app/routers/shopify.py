from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.shopify import CustomerProfileOut
from app.services.dependencies import get_current_agent, get_database
from app.services.shopify_service import ShopifyService

router = APIRouter(tags=["shopify"])


@router.get("/customers/{email}/profile", response_model=CustomerProfileOut)
async def customer_profile(
    email: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    _agent=Depends(get_current_agent),
):
    return await ShopifyService(db).fetch_customer_profile(email)
