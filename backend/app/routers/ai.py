from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.ai import AIReplyOut
from app.services.ai_service import AIService
from app.services.dependencies import get_current_agent, get_database

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/suggest-reply/{ticket_id}", response_model=AIReplyOut)
async def suggest_reply(
    ticket_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    _agent=Depends(get_current_agent),
):
    try:
        return await AIService(db).suggest_reply(ticket_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
