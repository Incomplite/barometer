from src.entities.cocktail.dependencies.repositories import CocktailRepositoryDI
from src.entities.cocktail.schemas import (
    CocktailCreateSchema,
    CocktailResponseSchema,
    CocktailUpdateSchema,
)


class CocktailService:
    def __init__(
        self,
        cocktail_repository: CocktailRepositoryDI,
    ) -> None:
        self._cocktail_repository = cocktail_repository

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
