from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import DatabaseSessionDI
from src.entities.cocktail.exceptions import CocktailNotFoundError
from src.entities.cocktail.models import CocktailModel


class CocktailRepository:
    model = CocktailModel

    def __init__(self, db_session: DatabaseSessionDI) -> None:
        self._session: AsyncSession = db_session

    async def get_cocktail_by_id(
        self,
        cocktail_id: int,
    ) -> CocktailModel:
        query = select(self.model).where(self.model.id == cocktail_id)
        cocktail = await self._session.scalar(query)
        if cocktail is None:
            raise CocktailNotFoundError
        return cocktail

    async def get_all_cocktails(self) -> Sequence[CocktailModel]:
        query = select(self.model)
        results = await self._session.scalars(query)
        return results.all()

    async def create_cocktail(
        self,
        cocktail_data: dict[str, Any],
    ) -> CocktailModel:
        cocktail_model = self.model(**cocktail_data)
        self._session.add(cocktail_model)
        await self._session.commit()
        return cocktail_model

    async def update_cocktail(
        self,
        cocktail_id: int,
        update_data: dict[str, Any],
    ) -> CocktailModel:
        cocktail = await self.get_cocktail_by_id(cocktail_id=cocktail_id)
        for key, value in update_data.items():
            setattr(cocktail, key, value)
        await self._session.commit()
        await self._session.refresh(cocktail)
        return cocktail

    async def delete_cocktail(self, cocktail_id: int) -> bool:
        try:
            cocktail = await self.get_cocktail_by_id(cocktail_id=cocktail_id)
            await self._session.delete(cocktail)
            await self._session.commit()
            return True
        except CocktailNotFoundError:
            return False
