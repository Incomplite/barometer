from src.entities.tag.dependencies.repositories import TagRepositoryDI
from src.entities.tag.exceptions import TagAlreadyExistsError
from src.entities.tag.schemas import (
    TagCreateSchema,
    TagResponseSchema,
    TagUpdateSchema,
)


class TagService:
    def __init__(
        self,
        tag_repository: TagRepositoryDI,
    ) -> None:
        self._tag_repository = tag_repository

    async def get_tag_by_id(
        self,
        tag_id: int,
    ) -> TagResponseSchema:
        tag = await self._tag_repository.get_tag_by_id(tag_id)
        return TagResponseSchema.model_validate(tag)

    async def get_all_tags(self) -> list[TagResponseSchema]:
        tags = await self._tag_repository.get_all_tags()
        return [TagResponseSchema.model_validate(tag) for tag in tags]

    async def create_tag(
        self,
        tag: TagCreateSchema,
    ) -> TagResponseSchema:
        existing_bar = await self._tag_repository.get_tag_by_name(
            tag_name=tag.name,
        )
        if existing_bar is not None:
            raise TagAlreadyExistsError
        tag_model = await self._tag_repository.create_tag(
            tag_data=tag,
        )
        return TagResponseSchema.model_validate(tag_model)

    async def update_tag(
        self,
        tag_id: int,
        tag_data: TagUpdateSchema,
    ) -> TagResponseSchema:
        update_data = tag_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )
        updated_tag = await self._tag_repository.update_tag(
            tag_id=tag_id,
            update_data=update_data,
        )

        return TagResponseSchema.model_validate(updated_tag)

    async def delete_tag(
        self,
        tag_id: int,
    ) -> bool:
        return await self._tag_repository.delete_tag(tag_id)
