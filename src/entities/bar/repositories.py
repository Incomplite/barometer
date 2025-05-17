from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.dependencies import DatabaseSessionDI
from src.entities.bar.exceptions import BarNotFoundError
from src.entities.bar.models import BarGalleryModel, BarModel, ReviewBarModel
from src.entities.tag.models import TagModel
from src.entities.user.models import UserFavoriteBarAssociation, UserModel


class BarRepository:
    model = BarModel

    def __init__(self, db_session: DatabaseSessionDI) -> None:
        self._session: AsyncSession = db_session

    async def get_bar_by_id(
        self,
        bar_id: int,
    ) -> BarModel:
        query = (
            select(self.model)
            .where(self.model.id == bar_id)
            .options(
                selectinload(self.model.gallery),
                selectinload(self.model.reviews),
                selectinload(self.model.tags),
                selectinload(self.model.favorited_by),
            )
        )
        bar = await self._session.scalar(query)

        if bar is None:
            raise BarNotFoundError

        return bar

    async def get_bar_by_name(
        self,
        name: str,
    ) -> BarModel | None:
        query = select(self.model).where(self.model.name == name)
        return await self._session.scalar(query)

    async def get_all_bars(self) -> Sequence[BarModel]:
        query = select(self.model).options(
            selectinload(self.model.gallery),
            selectinload(self.model.reviews),
            selectinload(self.model.tags),
            selectinload(self.model.favorited_by),
        )
        results = await self._session.scalars(query)
        return results.all()

    async def create_bar(
        self,
        bar_data: dict[str, Any],
    ) -> BarModel:
        bar_model = self.model(**bar_data)
        self._session.add(bar_model)
        await self._session.commit()
        await self._session.refresh(bar_model)

        bar_in_db = await self.get_bar_by_id(
            bar_id=bar_model.id,
        )

        return bar_in_db

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

    async def add_to_favorites(
        self,
        bar_id: int,
        user_id: int,
    ) -> None:
        bar = await self.get_bar_by_id(
            bar_id=bar_id,
        )
        user = await self._session.get(UserModel, user_id)
        if user is None:
            raise ValueError("User not found")

        if user not in bar.favorited_by:
            bar.favorited_by.append(user)
            await self._session.commit()
            await self._session.refresh(bar)

    async def remove_from_favorites(
        self,
        bar_id: int,
        user_id: int,
    ) -> None:
        bar = await self.get_bar_by_id(
            bar_id=bar_id,
        )
        user = await self._session.get(UserModel, user_id)
        if user in bar.favorited_by:
            bar.favorited_by.remove(user)
            await self._session.commit()

    async def get_user_favorite_bars(
        self,
        user_id: int,
    ) -> Sequence[BarModel]:
        query = (
            select(BarModel)
            .join(UserFavoriteBarAssociation)
            .where(UserFavoriteBarAssociation.user_id == user_id)
            .options(
                selectinload(self.model.gallery),
                selectinload(self.model.reviews),
                selectinload(self.model.tags),
                selectinload(self.model.favorited_by),
            )
        )
        results = await self._session.scalars(query)
        return results.all()

    async def add_review(
        self,
        bar_id: int,
        review_data: dict[str, Any],
    ) -> ReviewBarModel:
        bar = await self.get_bar_by_id(
            bar_id=bar_id,
        )
        review = ReviewBarModel(
            **review_data,
            bar_id=bar_id,
        )
        self._session.add(review)
        await self._session.commit()
        await self._session.refresh(review)
        return review

    async def get_reviews(
        self,
        bar_id: int,
    ) -> Sequence[ReviewBarModel]:
        query = select(ReviewBarModel).where(ReviewBarModel.bar_id == bar_id)
        results = await self._session.scalars(query)
        return results.all()

    async def add_gallery_image(
        self,
        bar_id: int,
        image_url: str,
    ) -> BarGalleryModel:
        bar = await self.get_bar_by_id(
            bar_id=bar_id,
        )
        gallery_image = BarGalleryModel(
            image_url=image_url,
            bar_id=bar_id,
        )
        self._session.add(gallery_image)
        await self._session.commit()
        await self._session.refresh(gallery_image)
        return gallery_image

    async def get_gallery(
        self,
        bar_id: int,
    ) -> Sequence[BarGalleryModel]:
        query = select(BarGalleryModel).where(BarGalleryModel.bar_id == bar_id)
        results = await self._session.scalars(query)
        return results.all()

    async def add_tag(
        self,
        bar_id: int,
        tag_id: int,
    ) -> None:
        bar = await self.get_bar_by_id(
            bar_id=bar_id,
        )
        tag = await self._session.get(TagModel, tag_id)
        if tag not in bar.tags:
            bar.tags.append(tag)
            await self._session.commit()

    async def remove_tag(
        self,
        bar_id: int,
        tag_id: int,
    ) -> None:
        bar = await self.get_bar_by_id(
            bar_id=bar_id,
        )
        tag = await self._session.get(TagModel, tag_id)
        if tag in bar.tags:
            bar.tags.remove(tag)
            await self._session.commit()

    async def get_tags(
        self,
        bar_id: int,
    ) -> Sequence[TagModel]:
        bar = await self.get_bar_by_id(
            bar_id=bar_id,
        )
        return bar.tags
