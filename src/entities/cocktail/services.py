from typing import Any, Sequence

from src.core.dependencies import DatabaseSessionDI
from src.entities.cocktail.dependencies.repositories import CocktailRepositoryDI
from src.entities.cocktail.models import (
    CocktailGalleryModel,
    ReviewCocktailModel,
)
from src.entities.cocktail.repositories import CocktailRepository
from src.entities.cocktail.schemas import (
    CocktailCreateSchema,
    CocktailResponseSchema,
    CocktailUpdateSchema,
)


class CocktailService:
    def __init__(
        self,
        cocktail_repository: CocktailRepositoryDI,
        db_session: DatabaseSessionDI,
    ) -> None:
        self._cocktail_repository = cocktail_repository
        self._repository = CocktailRepository(db_session)

    async def get_cocktail_by_id(
        self,
        cocktail_id: int,
    ) -> CocktailResponseSchema:
        cocktail = await self._cocktail_repository.get_cocktail_by_id(
            cocktail_id=cocktail_id,
        )
        return CocktailResponseSchema.model_validate(cocktail)

    async def get_all_cocktails(self) -> list[CocktailResponseSchema]:
        cocktails = await self._cocktail_repository.get_all_cocktails()
        return [
            CocktailResponseSchema.model_validate(cocktail) for cocktail in cocktails
        ]

    async def create_cocktail(
        self,
        cocktail: CocktailCreateSchema,
    ) -> CocktailResponseSchema:
        cocktail_model = await self._cocktail_repository.create_cocktail(
            cocktail.model_dump()
        )
        return CocktailResponseSchema.model_validate(cocktail_model)

    async def update_cocktail(
        self,
        cocktail_id: int,
        cocktail_data: CocktailUpdateSchema,
    ) -> CocktailResponseSchema:
        update_data = cocktail_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )
        updated_cocktail = await self._cocktail_repository.update_cocktail(
            cocktail_id=cocktail_id,
            update_data=update_data,
        )
        return CocktailResponseSchema.model_validate(updated_cocktail)

    async def delete_cocktail(
        self,
        cocktail_id: int,
    ) -> bool:
        return await self._cocktail_repository.delete_cocktail(cocktail_id)

    async def add_review(
        self, cocktail_id: int, review_data: dict[str, Any]
    ) -> ReviewCocktailModel:
        review = await self._repository.add_review(cocktail_id, review_data)
        # Update cocktail rating
        cocktail = await self._repository.get_cocktail_by_id(cocktail_id)
        reviews = await self._repository.get_reviews(cocktail_id)
        if reviews:
            cocktail.rating = sum(r.rating for r in reviews) / len(reviews)
            await self._repository.update_cocktail(
                cocktail_id, {"rating": cocktail.rating}
            )
        return review

    async def get_reviews(self, cocktail_id: int) -> Sequence[ReviewCocktailModel]:
        return await self._repository.get_reviews(cocktail_id)

    async def add_gallery_image(
        self, cocktail_id: int, image_url: str
    ) -> CocktailGalleryModel:
        return await self._repository.add_gallery_image(cocktail_id, image_url)

    async def get_gallery(self, cocktail_id: int) -> Sequence[CocktailGalleryModel]:
        return await self._repository.get_gallery(cocktail_id)
