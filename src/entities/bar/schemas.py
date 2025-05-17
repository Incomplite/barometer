from pydantic import BaseModel


class BarBaseSchema(BaseModel):
    name: str
    address: str


class BarCreateSchema(BarBaseSchema):
    pass


class BarUpdateSchema(BaseModel):
    name: str | None = None
    address: str | None = None


class BarResponseSchema(BarBaseSchema):
    id: int
