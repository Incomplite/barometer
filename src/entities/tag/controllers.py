from fastapi import APIRouter

from src.entities.tag.dependencies.services import TagServiceDI
from src.entities.tag.exceptions import (
    TagAlreadyExistsError,
    TagAlreadyExistsException,
    TagNotFoundError,
    TagNotFoundException,
)
from src.entities.tag.schemas import (
    TagCreateSchema,
    TagResponseSchema,
    TagUpdateSchema,
)

tag_router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
)


@tag_router.post(
    "/",
    response_model=TagResponseSchema,
)
async def create_tag(
    service: TagServiceDI,
    tag_data: TagCreateSchema,
):
    try:
        return await service.create_tag(
            tag=tag_data,
        )
    except TagAlreadyExistsError:
        raise TagAlreadyExistsException


@tag_router.get(
    "/",
    response_model=list[TagResponseSchema],
)
async def get_tags(service: TagServiceDI):
    return await service.get_all_tags()


@tag_router.get(
    "/{tag_id}",
    response_model=TagResponseSchema,
)
async def get_tag_by_id(
    service: TagServiceDI,
    tag_id: int,
):
    try:
        return await service.get_tag_by_id(tag_id)
    except TagNotFoundError:
        raise TagNotFoundException


@tag_router.patch(
    "/{tag_id}",
    response_model=TagResponseSchema,
)
async def update_tag(
    service: TagServiceDI,
    tag_id: int,
    tag_data: TagUpdateSchema,
):
    try:
        return await service.update_tag(
            tag_id=tag_id,
            tag_data=tag_data,
        )
    except TagNotFoundError:
        raise TagNotFoundException


@tag_router.delete(
    "/{tag_id}",
)
async def delete_tag(
    service: TagServiceDI,
    tag_id: int,
):
    await service.delete_tag(tag_id=tag_id)
    return {"message": "Tag deleted successfully"}
