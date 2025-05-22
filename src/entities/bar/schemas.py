from datetime import datetime
from typing import Optional

from pydantic import Field

from src.core.schemas.base import BaseSchema


class BarBaseSchema(BaseSchema):
    name: str = Field(..., max_length=50)
    description: Optional[str] = None
    address: str = Field(..., max_length=200)
    phone: str = Field(..., max_length=20)


class BarCreateSchema(BarBaseSchema):
    pass


class BarUpdateSchema(BarBaseSchema):
    name: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)


class BarGallerySchema(BaseSchema):
    id: int
    image_url: str = Field(..., max_length=200)
    bar_id: int


class ReviewBarResponseSchema(BaseSchema):
    id: int
    text: Optional[str] = None
    rating: Optional[float] = None
    # bar_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class ReviewBarCreateSchema(BaseSchema):
    text: Optional[str] = None
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")


class BarResponseSchema(BarBaseSchema):
    id: int
    rating: Optional[float] = None
    gallery: list[BarGallerySchema] = []
    reviews: list[ReviewBarResponseSchema] = []
    tags: list["TagResponseSchema"] = []


class BarCocktailsResponseSchema(BaseSchema):
    id: int
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    ingredients: str
    recipe: str
    video_url: Optional[str] = Field(None, max_length=200)
    rating: Optional[float] = None


# Import here to avoid circular imports
from src.entities.tag.schemas import TagResponseSchema  # noqa: E402
