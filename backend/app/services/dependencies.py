from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.mongo import get_db
from app.middleware.security import SecurityService

bearer_scheme = HTTPBearer(auto_error=True)


async def get_database() -> AsyncIOMotorDatabase:
    return get_db()


async def get_current_agent(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    token = credentials.credentials
    try:
        payload = SecurityService.decode_token(token)
        email = payload.get("sub")
        if not email:
            raise ValueError("Missing subject")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    agent = await db.agents.find_one({"email": email})
    if not agent:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Agent not found")
    agent["id"] = str(agent["_id"])
    return agent
