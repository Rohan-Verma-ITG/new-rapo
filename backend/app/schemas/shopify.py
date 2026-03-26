from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr


class CustomerProfileOut(BaseModel):
    email: EmailStr
    customer_snapshot: dict[str, Any]
    orders_snapshot: list[dict[str, Any]]
    synced_at: datetime
