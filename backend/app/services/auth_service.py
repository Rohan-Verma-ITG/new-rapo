from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.middleware.security import SecurityService


class AuthService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def login(self, email: str, password: str) -> str:
        agent = await self.db.agents.find_one({"email": email})
        if not agent:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        if not SecurityService.verify_password(password, agent["password_hash"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        return SecurityService.create_access_token(email)
