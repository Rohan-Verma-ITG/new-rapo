from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.ticket import MessageCreate, MessageOut, TicketCreate, TicketOut, TicketPatch
from app.services.dependencies import get_current_agent, get_database
from app.services.ticket_service import TicketService

router = APIRouter(tags=["tickets"])


@router.get("/tickets", response_model=list[TicketOut])
async def get_tickets(
    status: str | None = Query(default=None),
    priority: str | None = Query(default=None),
    assignee_id: str | None = Query(default=None),
    db: AsyncIOMotorDatabase = Depends(get_database),
    _agent=Depends(get_current_agent),
):
    return await TicketService(db).list_tickets(
        {"status": status, "priority": priority, "assignee_id": assignee_id}
    )


@router.post("/tickets", response_model=TicketOut)
async def create_ticket(
    payload: TicketCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    agent=Depends(get_current_agent),
):
    return await TicketService(db).create_ticket(payload.model_dump(), source="manual", actor=agent["email"])


@router.get("/tickets/{ticket_id}", response_model=TicketOut)
async def get_ticket(
    ticket_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    _agent=Depends(get_current_agent),
):
    ticket = await TicketService(db).get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.patch("/tickets/{ticket_id}", response_model=TicketOut)
async def patch_ticket(
    ticket_id: str,
    payload: TicketPatch,
    db: AsyncIOMotorDatabase = Depends(get_database),
    agent=Depends(get_current_agent),
):
    ticket = await TicketService(db).patch_ticket(ticket_id, payload.model_dump(), actor=agent["email"])
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.get("/tickets/{ticket_id}/messages", response_model=list[MessageOut])
async def list_messages(
    ticket_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    _agent=Depends(get_current_agent),
):
    return await TicketService(db).list_messages(ticket_id)


@router.post("/tickets/{ticket_id}/messages", response_model=MessageOut)
async def create_message(
    ticket_id: str,
    payload: MessageCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    agent=Depends(get_current_agent),
):
    return await TicketService(db).append_message(ticket_id, payload.model_dump(), actor=agent["email"])
