from typing import Sequence

from src.entities.bar.dependencies.repositories import BarRepositoryDI
from src.entities.bar.exceptions import BarAlreadyExistsError, UserAlreadyReviewedError
from src.entities.bar.models import BarGalleryModel, ReviewBarModel
from src.entities.bar.schemas import (
    BarCocktailsResponseSchema,
    BarCreateSchema,
    BarResponseSchema,
    BarUpdateSchema,
    ReviewBarCreateSchema,
    ReviewBarResponseSchema,
)
from src.entities.tag.dependencies.repositories import TagRepositoryDI
from src.entities.tag.schemas import TagResponseSchema


class BarService:
    def __init__(
        self,
        bar_repository: BarRepositoryDI,
        tag_repository: TagRepositoryDI,
    ) -> None:
        self._bar_repository = bar_repository
        self._tag_repository = tag_repository

    async def get_all_bars(self) -> list[BarResponseSchema]:
        bars = await self._bar_repository.get_all_bars()
        return [BarResponseSchema.model_validate(bar) for bar in bars]

    async def get_bar_by_id(
        self,
        bar_id: int,
    ) -> BarResponseSchema:
        bar = await self._bar_repository.get_bar_by_id(
            bar_id=bar_id,
        )
        return BarResponseSchema.model_validate(bar)

    async def create_bar(
        self,
        bar: BarCreateSchema,
    ) -> BarResponseSchema:
        existing_bar = await self._bar_repository.get_bar_by_name(name=bar.name)
        if existing_bar is not None:
            raise BarAlreadyExistsError
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

    async def delete_bar(
        self,
        bar_id: int,
    ) -> bool:
        return await self._bar_repository.delete_bar(bar_id)

    async def add_to_favorites(
        self,
        bar_id: int,
        user_id: int,
    ) -> None:
        bar = await self.get_bar_by_id(
            bar_id=bar_id,
        )
        await self._bar_repository.add_to_favorites(
            bar_id=bar.id,
            user_id=user_id,
        )

    async def remove_from_favorites(
        self,
        bar_id: int,
        user_id: int,
    ) -> None:
        await self._bar_repository.remove_from_favorites(
            bar_id=bar_id,
            user_id=user_id,
        )

    async def get_user_favorite_bars(
        self,
        user_id: int,
    ) -> list[BarResponseSchema]:
        bars = await self._bar_repository.get_user_favorite_bars(
            user_id=user_id,
        )

        return [BarResponseSchema.model_validate(bar) for bar in bars]

    async def add_review(
        self,
        bar_id: int,
        review_data: ReviewBarCreateSchema,
        user_id: int,
    ) -> ReviewBarResponseSchema:
        bar = await self._bar_repository.get_bar_by_id(
            bar_id=bar_id,
        )
        existing_review = next(
            (review for review in bar.reviews if review.user_id == user_id),
            None,
        )
        if existing_review:
            raise UserAlreadyReviewedError

        review_dict = review_data.model_dump()
        review_dict["user_id"] = user_id

        review = await self._bar_repository.add_review(
            bar_id=bar_id,
            review_data=review_dict,
        )

        reviews = await self._bar_repository.get_reviews(
            bar_id=bar_id,
        )
        if reviews:
            avg_rating = round(sum(r.rating for r in reviews) / len(reviews), 2)
            await self._bar_repository.update_bar(
                bar_id=bar_id,
                update_data={"rating": avg_rating},
            )

        return ReviewBarResponseSchema.model_validate(review)

    async def get_reviews(
        self,
        bar_id: int,
    ) -> Sequence[ReviewBarModel]:
        return await self._bar_repository.get_reviews(
            bar_id=bar_id,
        )

    async def add_gallery_image(
        self,
        bar_id: int,
        image_url: str,
    ) -> BarGalleryModel:
        return await self._bar_repository.add_gallery_image(
            bar_id=bar_id,
            image_url=image_url,
        )

    async def get_gallery(
        self,
        bar_id: int,
    ) -> Sequence[BarGalleryModel]:
        return await self._bar_repository.get_gallery(
            bar_id=bar_id,
        )

    async def add_tag(
        self,
        bar_id: int,
        tag_id: int,
    ) -> None:
        tag = await self._tag_repository.get_tag_by_id(
            tag_id=tag_id,
        )
        await self._bar_repository.add_tag(
            bar_id=bar_id,
            tag=tag,
        )

    async def remove_tag(
        self,
        bar_id: int,
        tag_id: int,
    ) -> None:
        tag = await self._tag_repository.get_tag_by_id(
            tag_id=tag_id,
        )
        await self._bar_repository.remove_tag(
            bar_id=bar_id,
            tag=tag,
        )

    async def get_tags(
        self,
        bar_id: int,
    ) -> Sequence[TagResponseSchema]:
        tags = await self._bar_repository.get_tags(
            bar_id=bar_id,
        )

        return [TagResponseSchema.model_validate(tag) for tag in tags]

    async def get_cocktails(
        self,
        bar_id: int,
    ) -> Sequence[BarCocktailsResponseSchema]:
        cocktails = await self._bar_repository.get_cocktails(
            bar_id=bar_id,
        )

        return [
            BarCocktailsResponseSchema.model_validate(cocktail)
            for cocktail in cocktails
        ]
