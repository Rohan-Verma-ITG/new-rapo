from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AgentOut(BaseModel):
    id: str
    email: EmailStr
    name: str
    role: str = "agent"
