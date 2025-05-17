from typing import Annotated

from fastapi import Depends

from src.entities.cocktail.repositories import CocktailRepository

CocktailRepositoryDI = Annotated[CocktailRepository, Depends(CocktailRepository)]
