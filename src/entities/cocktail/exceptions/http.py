from fastapi import status

from src.core.exceptions import BaseException


class CocktailNotFoundException(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Cocktail not found"


class CocktailAlreadyExistsException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Cocktail already exists"
