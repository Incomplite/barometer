from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from src.auth.dependencies.auth_module import CurrentUserDI
from src.entities.bar.dependencies.services import BarServiceDI
from src.entities.bar.exceptions import (
    BarAlreadyExistsError,
    BarAlreadyExistsException,
    BarNotFoundError,
    BarNotFoundException,
)
from src.entities.bar.schemas import (
    BarCreateSchema,
    BarGallerySchema,
    BarResponseSchema,
    BarUpdateSchema,
    ReviewBarCreateSchema,
    ReviewBarResponseSchema,
)
from src.entities.tag.schemas import TagResponseSchema

bar_router = APIRouter(
    prefix="/bars",
    tags=["Bars"],
)

# ======
# GET/Read
# ======


@bar_router.get(
    "/",
    response_model=list[BarResponseSchema],
)
async def get_all_bars(
    bar_service: BarServiceDI,
):
    return await bar_service.get_all_bars()


@bar_router.get(
    "/{bar_id}",
    response_model=BarResponseSchema,
)
async def get_bar_by_id(
    bar_service: BarServiceDI,
    bar_id: int,
):
    try:
        return await bar_service.get_bar_by_id(
            bar_id=bar_id,
        )
    except BarNotFoundError:
        raise BarNotFoundException


# ======
# POST/Create
# ======


@bar_router.post(
    "/",
    response_model=BarResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_bar(
    bar_service: BarServiceDI,
    bar: BarCreateSchema,
):
    try:
        return await bar_service.create_bar(bar=bar)
    except BarAlreadyExistsError:
        raise BarAlreadyExistsException


@bar_router.post(
    "/{bar_id}/favorites/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def add_to_favorites(
    bar_service: BarServiceDI,
    user: CurrentUserDI,
    bar_id: int,
):
    try:
        await bar_service.add_to_favorites(
            bar_id=bar_id,
            user_id=user.id,
        )

        return JSONResponse(
            {
                "message": "Bar added to favorites successfully",
            }
        )
    except BarNotFoundError:
        raise BarNotFoundException


# ======
# PUT/PATCH/Update
# ======


@bar_router.patch(
    "/{bar_id}",
    response_model=BarResponseSchema,
)
async def update_bar(
    bar_service: BarServiceDI,
    bar_id: int,
    bar: BarUpdateSchema,
):
    try:
        return await bar_service.update_bar(
            bar_id=bar_id,
            bar_data=bar,
        )
    except BarNotFoundError:
        raise BarNotFoundException


# ======
# Delete
# ======


@bar_router.delete(
    "/{bar_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_bar(
    bar_service: BarServiceDI,
    bar_id: int,
):
    try:
        await bar_service.delete_bar(bar_id=bar_id)

        return JSONResponse(
            {
                "message": "Bar successfully removed",
            }
        )
    except BarNotFoundError:
        raise BarNotFoundException


@bar_router.delete(
    "/{bar_id}/favorites/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_from_favorites(
    bar_service: BarServiceDI,
    user: CurrentUserDI,
    bar_id: int,
):
    try:
        await bar_service.remove_from_favorites(
            bar_id=bar_id,
            user_id=user.id,
        )

        return JSONResponse(
            {
                "message": "Bar successfully removed from favorites",
            }
        )
    except BarNotFoundError:
        raise BarNotFoundException


# Reviews endpoints
@bar_router.post(
    "/{bar_id}/reviews",
    response_model=ReviewBarResponseSchema,
)
async def add_review(
    bar_service: BarServiceDI,
    user: CurrentUserDI,
    bar_id: int,
    review: ReviewBarCreateSchema,
):
    try:
        return await bar_service.add_review(
            bar_id=bar_id,
            review_data=review.model_dump(),
            user_id=user.id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@bar_router.get(
    "/{bar_id}/reviews",
    response_model=list[ReviewBarResponseSchema],
)
async def get_reviews(
    bar_service: BarServiceDI,
    bar_id: int,
):
    return await bar_service.get_reviews(
        bar_id=bar_id,
    )


# Gallery endpoints
@bar_router.post(
    "/{bar_id}/gallery",
    response_model=BarGallerySchema,
)
async def add_gallery_image(
    bar_service: BarServiceDI,
    bar_id: int,
    image_url: str,
):
    return await bar_service.add_gallery_image(
        bar_id=bar_id,
        image_url=image_url,
    )


@bar_router.get(
    "/{bar_id}/gallery",
    response_model=list[BarGallerySchema],
)
async def get_gallery(
    bar_service: BarServiceDI,
    bar_id: int,
):
    return await bar_service.get_gallery(
        bar_id=bar_id,
    )


# Tags endpoints
@bar_router.post(
    "/{bar_id}/tags/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def add_tag(
    bar_service: BarServiceDI,
    bar_id: int,
    tag_id: int,
):
    await bar_service.add_tag(
        bar_id=bar_id,
        tag_id=tag_id,
    )


@bar_router.delete(
    "/{bar_id}/tags/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_tag(
    bar_service: BarServiceDI,
    bar_id: int,
    tag_id: int,
) -> None:
    await bar_service.remove_tag(
        bar_id=bar_id,
        tag_id=tag_id,
    )


@bar_router.get(
    "/{bar_id}/tags",
    response_model=list[TagResponseSchema],
)
async def get_tags(
    bar_service: BarServiceDI,
    bar_id: int,
) -> list[TagResponseSchema]:
    return await bar_service.get_tags(
        bar_id=bar_id,
    )
