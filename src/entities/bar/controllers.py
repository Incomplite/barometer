from fastapi import APIRouter

from src.entities.bar.dependencies.services import BarServiceDI
from src.entities.bar.exceptions import BarNotFoundError, BarNotFoundException
from src.entities.bar.schemas import (
    BarCreateSchema,
    BarResponseSchema,
    BarUpdateSchema,
)

bar_router = APIRouter(
    prefix="/bars",
    tags=["Bars"],
)


@bar_router.post(
    "/",
    response_model=BarResponseSchema,
)
async def create_bar(
    service: BarServiceDI,
    bar_data: BarCreateSchema,
):
    return await service.create_bar(bar_data)


@bar_router.get(
    "/",
    response_model=list[BarResponseSchema],
)
async def get_bars(service: BarServiceDI):
    return await service.get_all_bars()


@bar_router.get(
    "/{bar_id}",
    response_model=BarResponseSchema,
)
async def get_bar_by_id(
    service: BarServiceDI,
    bar_id: int,
):
    try:
        return await service.get_bar_by_id(bar_id=bar_id)
    except BarNotFoundError:
        raise BarNotFoundException


@bar_router.patch(
    "/{bar_id}",
    response_model=BarResponseSchema,
)
async def update_bar(
    service: BarServiceDI,
    bar_id: int,
    bar_data: BarUpdateSchema,
):
    try:
        return await service.update_bar(
            bar_id=bar_id,
            bar_data=bar_data,
        )
    except BarNotFoundError:
        raise BarNotFoundException


@bar_router.delete(
    "/{bar_id}",
)
async def delete_bar(
    service: BarServiceDI,
    bar_id: int,
):
    await service.delete_bar(bar_id)
    return {"message": "Bar deleted successfully"}
