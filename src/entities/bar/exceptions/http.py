from fastapi import status

from src.core.exceptions import BaseException


class BarNotFoundException(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Bar not found"


class BarAlreadyExistsException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Bar already exists"
