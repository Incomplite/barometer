from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from passlib.context import CryptContext

from src.auth.exceptions import InvalidTokenError, TokenExpiredError
from src.config import project_config
from src.entities.user.dependencies.repositories import UserRepositoryDI
from src.entities.user.schemas import UserResponseSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(
        self,
        user_repository: UserRepositoryDI,
    ) -> None:
        self._user_repository = user_repository

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    async def authenticate_user(
        self, username: str, password: str
    ) -> UserResponseSchema | None:
        user = await self._user_repository.get_user_by_username(username)
        if not user or not self.verify_password(password, user.password):
            return None
        return UserResponseSchema.model_validate(user)

    @staticmethod
    def create_access_token(user_data: dict) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=project_config.auth.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        data = {
            **user_data,
            "exp": expire,
            "type": "access",
        }
        return jwt.encode(
            data,
            project_config.auth.SECRET_KEY,
            algorithm=project_config.auth.ALGORITHM,
        )

    @staticmethod
    def create_refresh_token(user_data: dict) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            days=project_config.auth.REFRESH_TOKEN_EXPIRE_DAYS
        )
        data = {
            **user_data,
            "exp": expire,
            "type": "refresh",
        }
        return jwt.encode(
            data,
            project_config.auth.SECRET_KEY,
            algorithm=project_config.auth.ALGORITHM,
        )

    @staticmethod
    def verify_refresh_token(
        refresh_token: str,
    ) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                refresh_token,
                project_config.auth.SECRET_KEY,
                algorithms=[project_config.auth.ALGORITHM],
            )
            token_type: str | None = payload.get("type")

            if token_type != "refresh":  # nosec
                raise InvalidTokenError
            return payload
        except ExpiredSignatureError:
            raise TokenExpiredError
        except JWTError:
            raise InvalidTokenError
