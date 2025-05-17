from src.entities.bar.dependencies.repositories import BarRepositoryDI
from src.entities.bar.schemas import (
    BarCreateSchema,
    BarResponseSchema,
    BarUpdateSchema,
)


class BarService:
    def __init__(
        self,
        bar_repository: BarRepositoryDI,
    ) -> None:
        self._bar_repository = bar_repository

    async def get_bar_by_id(
        self,
        bar_id: int,
    ) -> BarResponseSchema:
        bar = await self._bar_repository.get_bar_by_id(bar_id)
        return BarResponseSchema.model_validate(bar)

    async def create_bar(
        self,
        bar: BarCreateSchema,
    ) -> BarResponseSchema:
        bar_model = await self._bar_repository.create_bar(bar.model_dump())
        return BarResponseSchema.model_validate(bar_model)

    async def update_bar(
        self,
        bar_id: int,
        bar_data: BarUpdateSchema,
    ) -> BarResponseSchema:
        update_data = bar_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )
        updated_bar = await self._bar_repository.update_bar(
            bar_id=bar_id,
            update_data=update_data,
        )
        return BarResponseSchema.model_validate(updated_bar)

    async def get_all_bars(self) -> list[BarResponseSchema]:
        bars = await self._bar_repository.get_all_bars()
        return [BarResponseSchema.model_validate(bar) for bar in bars]

    async def delete_bar(
        self,
        bar_id: int,
    ) -> bool:
        return await self._bar_repository.delete_bar(bar_id)
