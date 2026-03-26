from pydantic import BaseModel


class AIReplyOut(BaseModel):
    intent: str
    confidence: float
    suggested_reply: str
