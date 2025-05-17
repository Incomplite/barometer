from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class BarBaseSchema(BaseModel):
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


class BarGallerySchema(BaseModel):
    id: int
    image_url: str = Field(..., max_length=200)
    bar_id: int

    class Config:
        from_attributes = True


class ReviewBarResponseSchema(BaseModel):
    id: int
    text: str
    rating: Optional[float] = None
    bar_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReviewBarCreateSchema(BaseModel):
    text: str
    rating: int = Field(..., ge=0, le=5, description="Rating from 0 to 5")

    @field_validator("rating")
    def validate_rating(cls, v: int) -> int:
        if not 0 <= v <= 5:
            raise ValueError("Rating must be between 0 and 5")
        return v


class BarResponseSchema(BarBaseSchema):
    id: int
    rating: Optional[float] = None
    gallery: list[BarGallerySchema] = []
    reviews: list[ReviewBarResponseSchema] = []
    tags: list["TagResponseSchema"] = []

    class Config:
        from_attributes = True


# Import here to avoid circular imports
from src.entities.tag.schemas import TagResponseSchema  # noqa: E402
