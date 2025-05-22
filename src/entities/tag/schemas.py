from src.core.schemas.base import BaseSchema


class TagBaseSchema(BaseSchema):
    name: str


class TagCreateSchema(TagBaseSchema):
    pass


class TagUpdateSchema(TagBaseSchema):
    name: str | None = None


class TagResponseSchema(TagBaseSchema):
    id: int
