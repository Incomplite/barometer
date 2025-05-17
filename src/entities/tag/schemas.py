from pydantic import BaseModel


class TagBaseSchema(BaseModel):
    name: str


class TagCreateSchema(TagBaseSchema):
    pass


class TagUpdateSchema(TagBaseSchema):
    name: str | None = None


class TagResponseSchema(TagBaseSchema):
    id: int
