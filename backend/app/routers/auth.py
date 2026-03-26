from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.auth import AgentOut, LoginRequest, LoginResponse
from app.services.auth_service import AuthService
from app.services.dependencies import get_current_agent, get_database

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    token = await AuthService(db).login(payload.email, payload.password)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=AgentOut)
async def me(agent=Depends(get_current_agent)):
    return {
        "id": agent["id"],
        "email": agent["email"],
        "name": agent.get("name", ""),
        "role": agent.get("role", "agent"),
    }
