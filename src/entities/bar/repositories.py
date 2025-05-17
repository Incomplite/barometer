from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import DatabaseSessionDI
from src.entities.bar.exceptions import BarNotFoundError
from src.entities.bar.models import BarModel


class BarRepository:
    model = BarModel

    def __init__(self, db_session: DatabaseSessionDI) -> None:
        self._session: AsyncSession = db_session

    async def get_bar_by_id(
        self,
        bar_id: int,
    ) -> BarModel:
        query = select(self.model).where(self.model.id == bar_id)
        bar = await self._session.scalar(query)
        if bar is None:
            raise BarNotFoundError
        return bar

    async def get_all_bars(self) -> Sequence[BarModel]:
        query = select(self.model)
        results = await self._session.scalars(query)
        return results.all()

    async def create_bar(
        self,
        bar_data: dict[str, Any],
    ) -> BarModel:
        bar_model = self.model(**bar_data)
        self._session.add(bar_model)
        await self._session.commit()
        return bar_model

    async def update_bar(
        self,
        bar_id: int,
        update_data: dict[str, Any],
    ) -> BarModel:
        bar = await self.get_bar_by_id(bar_id=bar_id)
        for key, value in update_data.items():
            setattr(bar, key, value)
        await self._session.commit()
        await self._session.refresh(bar)
        return bar

    async def delete_bar(
        self,
        bar_id: int,
    ) -> bool:
        try:
            bar = await self.get_bar_by_id(bar_id=bar_id)
            await self._session.delete(bar)
            await self._session.commit()
            return True
        except BarNotFoundError:
            return False
