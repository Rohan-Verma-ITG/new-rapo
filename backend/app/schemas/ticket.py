from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.models.enums import TicketPriority, TicketStatus


class TicketCreate(BaseModel):
    subject: str
    customer_email: EmailStr
    status: TicketStatus = TicketStatus.open
    priority: TicketPriority = TicketPriority.medium
    tags: list[str] = Field(default_factory=list)


class TicketPatch(BaseModel):
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    assignee_id: Optional[str] = None
    tags: Optional[list[str]] = None


class TicketOut(BaseModel):
    id: str = Field(alias="_id")
    subject: str
    customer_email: EmailStr
    status: TicketStatus
    priority: TicketPriority
    assignee_id: Optional[str] = None
    tags: list[str]
    source: str
    sla_due_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"populate_by_name": True}


class MessageCreate(BaseModel):
    body: str
    sender_type: str = "agent"
    sender_email: EmailStr
    is_internal: bool = False


class MessageOut(BaseModel):
    id: str = Field(alias="_id")
    ticket_id: str
    body: str
    sender_type: str
    sender_email: EmailStr
    is_internal: bool
    created_at: datetime

    model_config = {"populate_by_name": True}
