from typing import Optional

from pydantic import BaseModel, Field


class CocktailBaseSchema(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    ingredients: str
    recipe: str
    video_url: Optional[str] = Field(None, max_length=200)


class CocktailCreateSchema(CocktailBaseSchema):
    bar_id: int


class CocktailUpdateSchema(CocktailBaseSchema):
    name: Optional[str] = Field(None, max_length=100)
    ingredients: Optional[str] = None
    recipe: Optional[str] = None
    video_url: Optional[str] = Field(None, max_length=200)
    bar_id: Optional[int] = None


class CocktailGallerySchema(BaseModel):
    id: int
    image_url: str = Field(..., max_length=200)
    cocktail_id: int

    class Config:
        from_attributes = True


class ReviewCocktailSchema(BaseModel):
    id: int
    text: str
    rating: Optional[float] = None
    cocktail_id: int

    class Config:
        from_attributes = True


class ReviewCocktailCreateSchema(BaseModel):
    text: str
    rating: Optional[float] = None


class CocktailResponseSchema(CocktailBaseSchema):
    id: int
    bar_id: int
    rating: Optional[float] = None
    gallery: list[CocktailGallerySchema] = []
    reviews: list[ReviewCocktailSchema] = []

    class Config:
        from_attributes = True
