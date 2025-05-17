from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import DatabaseSessionDI
from src.entities.tag.exceptions import TagNotFoundError
from src.entities.tag.models import TagModel
from src.entities.tag.schemas import TagCreateSchema


class TagRepository:
    model = TagModel

    def __init__(self, db_session: DatabaseSessionDI) -> None:
        self._session: AsyncSession = db_session

    async def get_tag_by_id(
        self,
        tag_id: int,
    ) -> TagModel:
        query = select(self.model).where(self.model.id == tag_id)
        tag = await self._session.scalar(query)

        if tag is None:
            raise TagNotFoundError

        return tag

    async def get_all_tags(self) -> Sequence[TagModel]:
        query = select(self.model)
        results = await self._session.scalars(query)
        return results.all()

    async def create_tag(
        self,
        tag: TagCreateSchema,
    ) -> TagModel:
        tag_model = self.model(**tag.model_dump())
        self._session.add(tag_model)
        await self._session.commit()
        return tag_model

    async def update_tag(
        self,
        tag_id: int,
        update_data: dict[str, Any],
    ) -> TagModel | None:
        tag = await self.get_tag_by_id(tag_id=tag_id)
        for key, value in update_data.items():
            setattr(tag, key, value)

            await self._session.commit()
            await self._session.refresh(tag)
        return tag

    async def delete_tag(
        self,
        tag_id: int,
    ) -> bool:
        try:
            tag = await self.get_tag_by_id(tag_id=tag_id)
            await self._session.delete(tag)
            await self._session.commit()
            return True
        except TagNotFoundError:
            return False
