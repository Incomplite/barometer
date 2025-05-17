from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError

from src.auth.exceptions import CredentialsException, TokenExpiredException
from src.config import project_config
from src.entities.user.dependencies.repositories import UserRepositoryDI
from src.entities.user.models import UserRoleEnum
from src.entities.user.schemas import UserResponseSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def get_current_user_role(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserRoleEnum:
    try:
        payload = jwt.decode(
            token,
            project_config.auth.SECRET_KEY,
            algorithms=[project_config.auth.ALGORITHM],
        )
        role: str | None = payload.get("role")
        if role is None:
            raise CredentialsException
        return UserRoleEnum(role)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise CredentialsException


async def get_current_user(
    user_repository: UserRepositoryDI,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserResponseSchema:
    try:
        payload = jwt.decode(
            token,
            project_config.auth.SECRET_KEY,
            algorithms=[project_config.auth.ALGORITHM],
        )
        user_id: int | None = payload.get("user_id")
        if user_id is None:
            raise CredentialsException
        user = await user_repository.get_user_by_id(user_id)
        if user is None:
            raise CredentialsException
        return UserResponseSchema.model_validate(user)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise CredentialsException
