from typing import Annotated

from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.dependencies.services import AuthServiceDI
from src.auth.exceptions import (
    InvalidCredentialsException,
    InvalidRefreshTokenException,
    InvalidTokenError,
    TokenExpiredError,
    TokenExpiredException,
)
from src.auth.schemas import TokenSchema

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@auth_router.post("/login", response_model=TokenSchema)
async def login(
    auth_service: AuthServiceDI,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise InvalidCredentialsException

    user_data = {
        "user_id": user.id,
        "sub": user.username,
        "role": user.role,
    }

    access_token = auth_service.create_access_token(user_data)
    refresh_token = auth_service.create_refresh_token(user_data)
    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


@auth_router.post("/refresh", response_model=TokenSchema)
async def refresh_token(
    auth_service: AuthServiceDI,
    refresh_token: str = Body(..., embed=True),
):
    try:
        payload = auth_service.verify_refresh_token(refresh_token)
    except TokenExpiredError:
        raise TokenExpiredException
    except InvalidTokenError:
        raise InvalidRefreshTokenException

    user_data = {
        "user_id": payload["user_id"],
        "sub": payload["sub"],
        "role": payload["role"],
    }

    new_access_token = auth_service.create_access_token(user_data)
    new_refresh_token = auth_service.create_refresh_token(user_data)

    return TokenSchema(access_token=new_access_token, refresh_token=new_refresh_token)
