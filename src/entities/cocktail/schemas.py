from typing import Optional

from pydantic import Field

from src.core.schemas.base import BaseSchema


class CocktailBaseSchema(BaseSchema):
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


class CocktailGallerySchema(BaseSchema):
    id: int
    image_url: str = Field(..., max_length=200)
    cocktail_id: int


class ReviewCocktailResponseSchema(BaseSchema):
    id: int
    text: Optional[str] = None
    rating: Optional[float] = None
    # cocktail_id: int
    user_id: int


class ReviewCocktailCreateSchema(BaseSchema):
    text: Optional[str] = None
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")


class CocktailResponseSchema(CocktailBaseSchema):
    id: int
    bar_id: int
    rating: Optional[float] = None
    gallery: list[CocktailGallerySchema] = []
    reviews: list[ReviewCocktailResponseSchema] = []
