from fastapi import APIRouter, status

from src.entities.cocktail.dependencies.services import CocktailServiceDI
from src.entities.cocktail.exceptions import (
    CocktailNotFoundError,
    CocktailNotFoundException,
)
from src.entities.cocktail.schemas import (
    CocktailCreateSchema,
    CocktailGallerySchema,
    CocktailResponseSchema,
    CocktailUpdateSchema,
    ReviewCocktailCreateSchema,
    ReviewCocktailSchema,
)

cocktail_router = APIRouter(
    prefix="/cocktails",
    tags=["Cocktails"],
)


@cocktail_router.get(
    "/",
    response_model=list[CocktailResponseSchema],
)
async def get_all_cocktails(
    cocktail_service: CocktailServiceDI,
):
    return await cocktail_service.get_all_cocktails()


@cocktail_router.get(
    "/{cocktail_id}",
    response_model=CocktailResponseSchema,
)
async def get_cocktail(
    cocktail_service: CocktailServiceDI,
    cocktail_id: int,
):
    try:
        return await cocktail_service.get_cocktail_by_id(
            cocktail_id=cocktail_id,
        )
    except CocktailNotFoundError:
        raise CocktailNotFoundException


@cocktail_router.post(
    "/",
    response_model=CocktailResponseSchema,
)
async def create_cocktail(
    cocktail_service: CocktailServiceDI,
    cocktail: CocktailCreateSchema,
):
    return await cocktail_service.create_cocktail(
        cocktail=cocktail,
    )


@cocktail_router.put(
    "/{cocktail_id}",
    response_model=CocktailResponseSchema,
)
async def update_cocktail(
    cocktail_service: CocktailServiceDI,
    cocktail_id: int,
    cocktail: CocktailUpdateSchema,
):
    try:
        return await cocktail_service.update_cocktail(
            cocktail_id=cocktail_id,
            cocktail_data=cocktail,
        )
    except CocktailNotFoundError:
        raise CocktailNotFoundException


@cocktail_router.delete(
    "/{cocktail_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_cocktail(
    cocktail_service: CocktailServiceDI,
    cocktail_id: int,
):
    await cocktail_service.delete_cocktail(
        cocktail_id=cocktail_id,
    )


# Reviews endpoints
@cocktail_router.post(
    "/{cocktail_id}/reviews",
    response_model=ReviewCocktailSchema,
)
async def add_review(
    cocktail_service: CocktailServiceDI,
    cocktail_id: int,
    review: ReviewCocktailCreateSchema,
):
    return await cocktail_service.add_review(
        cocktail_id=cocktail_id,
        review_data=review.model_dump(),
    )


@cocktail_router.get(
    "/{cocktail_id}/reviews",
    response_model=list[ReviewCocktailSchema],
)
async def get_reviews(
    cocktail_service: CocktailServiceDI,
    cocktail_id: int,
):
    return await cocktail_service.get_reviews(
        cocktail_id=cocktail_id,
    )


# Gallery endpoints
@cocktail_router.post(
    "/{cocktail_id}/gallery",
    response_model=CocktailGallerySchema,
)
async def add_gallery_image(
    cocktail_service: CocktailServiceDI,
    cocktail_id: int,
    image_url: str,
):
    return await cocktail_service.add_gallery_image(
        cocktail_id=cocktail_id,
        image_url=image_url,
    )


@cocktail_router.get(
    "/{cocktail_id}/gallery",
    response_model=list[CocktailGallerySchema],
)
async def get_gallery(
    cocktail_service: CocktailServiceDI,
    cocktail_id: int,
):
    return await cocktail_service.get_gallery(cocktail_id=cocktail_id)
