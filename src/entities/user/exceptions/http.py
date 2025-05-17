from fastapi import status
from src.core.exceptions import BaseException


class UserNotFoundException(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"


class UserAlreadyExistsException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"
