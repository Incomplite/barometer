from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.auth.dependencies.auth_module import CurrentUserDI
from src.entities.cocktail.dependencies.services import CocktailServiceDI
from src.entities.cocktail.exceptions import (
    CocktailNotFoundError,
    CocktailNotFoundException,
    UserAlreadyReviewedError,
    UserAlreadyReviewedException,
)
from src.entities.cocktail.schemas import (
    CocktailCreateSchema,
    CocktailGallerySchema,
    CocktailResponseSchema,
    CocktailUpdateSchema,
    ReviewCocktailCreateSchema,
    ReviewCocktailResponseSchema,
)

cocktail_router = APIRouter(
    prefix="/cocktails",
    tags=["Cocktails"],
)

# ======
# GET/Read
# ======


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
async def get_cocktail_by_id(
    cocktail_service: CocktailServiceDI,
    cocktail_id: int,
):
    try:
        return await cocktail_service.get_cocktail_by_id(
            cocktail_id=cocktail_id,
        )
    except CocktailNotFoundError:
        raise CocktailNotFoundException


@cocktail_router.get(
    "/{cocktail_id}/reviews",
    response_model=list[ReviewCocktailResponseSchema],
)
async def get_reviews(
    cocktail_service: CocktailServiceDI,
    cocktail_id: int,
):
    return await cocktail_service.get_reviews(
        cocktail_id=cocktail_id,
    )


@cocktail_router.get(
    "/{cocktail_id}/gallery",
    response_model=list[CocktailGallerySchema],
)
async def get_gallery(
    cocktail_service: CocktailServiceDI,
    cocktail_id: int,
):
    return await cocktail_service.get_gallery(
        cocktail_id=cocktail_id,
    )


# ======
# POST/Create
# ======


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


@cocktail_router.post(
    "/{cocktail_id}/reviews/",
    response_model=ReviewCocktailResponseSchema,
)
async def add_review(
    cocktail_service: CocktailServiceDI,
    user: CurrentUserDI,
    cocktail_id: int,
    review_data: ReviewCocktailCreateSchema,
):
    try:
        return await cocktail_service.add_review(
            cocktail_id=cocktail_id,
            review_data=review_data,
            user_id=user.id,
        )
    except UserAlreadyReviewedError:
        raise UserAlreadyReviewedException


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


# ======
# PUT/PATCH/Update
# ======


@cocktail_router.patch(
    "/{cocktail_id}",
    response_model=CocktailResponseSchema,
)
async def update_cocktail(
    cocktail_service: CocktailServiceDI,
    cocktail_id: int,
    cocktail_data: CocktailUpdateSchema,
):
    try:
        return await cocktail_service.update_cocktail(
            cocktail_id=cocktail_id,
            cocktail_data=cocktail_data,
        )
    except CocktailNotFoundError:
        raise CocktailNotFoundException


# ======
# Delete
# ======


@cocktail_router.delete(
    "/{cocktail_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_cocktail(
    cocktail_service: CocktailServiceDI,
    cocktail_id: int,
):
    try:
        await cocktail_service.delete_cocktail(
            cocktail_id=cocktail_id,
        )
        return JSONResponse(
            {
                "message": "Cocktail successfully removed",
            }
        )
    except CocktailNotFoundError:
        raise CocktailNotFoundException
