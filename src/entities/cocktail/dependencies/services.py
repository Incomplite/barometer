from typing import Annotated

from fastapi import Depends

from src.entities.cocktail.services import CocktailService

CocktailServiceDI = Annotated[CocktailService, Depends(CocktailService)]
