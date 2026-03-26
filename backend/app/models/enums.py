from enum import Enum


class TicketStatus(str, Enum):
    open = "open"
    pending = "pending"
    resolved = "resolved"
    closed = "closed"


class TicketPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"
