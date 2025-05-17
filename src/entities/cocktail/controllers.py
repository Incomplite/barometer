from fastapi import APIRouter

from src.entities.cocktail.dependencies.services import CocktailServiceDI
from src.entities.cocktail.exceptions import (
    CocktailNotFoundError,
    CocktailNotFoundException,
)
from src.entities.cocktail.schemas import (
    CocktailCreateSchema,
    CocktailResponseSchema,
    CocktailUpdateSchema,
)

cocktail_router = APIRouter(
    prefix="/cocktails",
    tags=["Cocktails"],
)


@cocktail_router.post(
    "/",
    response_model=CocktailResponseSchema,
)
async def create_cocktail(
    service: CocktailServiceDI,
    cocktail_data: CocktailCreateSchema,
):
    return await service.create_cocktail(cocktail_data)


@cocktail_router.get(
    "/",
    response_model=list[CocktailResponseSchema],
)
async def get_cocktails(service: CocktailServiceDI):
    return await service.get_all_cocktails()


@cocktail_router.get(
    "/{cocktail_id}",
    response_model=CocktailResponseSchema,
)
async def get_cocktail_by_id(
    service: CocktailServiceDI,
    cocktail_id: int,
):
    try:
        return await service.get_cocktail_by_id(cocktail_id)
    except CocktailNotFoundError:
        raise CocktailNotFoundException


@cocktail_router.patch(
    "/{cocktail_id}",
    response_model=CocktailResponseSchema,
)
async def update_cocktail(
    service: CocktailServiceDI,
    cocktail_id: int,
    cocktail_data: CocktailUpdateSchema,
):
    try:
        return await service.update_cocktail(
            cocktail_id=cocktail_id,
            cocktail_data=cocktail_data,
        )
    except CocktailNotFoundError:
        raise CocktailNotFoundException


@cocktail_router.delete(
    "/{cocktail_id}",
)
async def delete_cocktail(
    service: CocktailServiceDI,
    cocktail_id: int,
):
    await service.delete_cocktail(cocktail_id)
    return {"message": "Cocktail deleted successfully"}
