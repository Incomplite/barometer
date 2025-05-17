from fastapi import status

from src.core.exceptions import BaseException


class TagNotFoundException(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Tag not found"


class TagAlreadyExistsException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Tag already exists"
