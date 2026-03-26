import hashlib
import hmac
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SecurityService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(subject: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_exp_minutes)
        payload = {"sub": subject, "exp": expire}
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        except JWTError as exc:
            raise ValueError("Invalid token") from exc

    @staticmethod
    def verify_shopify_hmac(data: bytes, hmac_header: str) -> bool:
        digest = hmac.new(
            settings.shopify_webhook_secret.encode("utf-8"), data, hashlib.sha256
        ).digest()
        generated_hmac = digest.hex()
        return hmac.compare_digest(generated_hmac, hmac_header)

    @staticmethod
    def verify_mailgun_signature(timestamp: str, token: str, signature: str) -> bool:
        value = f"{timestamp}{token}".encode("utf-8")
        digest = hmac.new(settings.mailgun_signing_key.encode("utf-8"), value, hashlib.sha256)
        return hmac.compare_digest(digest.hexdigest(), signature)
