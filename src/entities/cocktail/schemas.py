from pydantic import BaseModel


class CocktailBaseSchema(BaseModel):
    name: str
    description: str


class CocktailCreateSchema(CocktailBaseSchema):
    pass


class CocktailUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None


class CocktailResponseSchema(CocktailBaseSchema):
    id: int
