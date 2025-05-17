from fastapi import status
from src.core.exceptions import BaseException


class CredentialsException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Could not validate credentials"
    headers = {"WWW-Authenticate": "Bearer"}


class InvalidCredentialsException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect username or password"


class InvalidRefreshTokenException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid refresh token"


class TokenExpiredException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token expires"


class AdminRequiredException(BaseException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "This operation is only available for admins"


class UserRequiredException(BaseException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "This operation is only available for users"

