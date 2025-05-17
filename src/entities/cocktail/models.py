from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db_helpers import Base


class CocktailModel(Base):
    __tablename__ = "cocktails"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    ingredients: Mapped[str] = mapped_column(Text)
    recipe: Mapped[str] = mapped_column(Text)
    video_url: Mapped[str] = mapped_column(String(200), nullable=True)
    rating: Mapped[float] = mapped_column(nullable=True)
    bar_id: Mapped[int] = mapped_column(ForeignKey("bars.id"))

    gallery = relationship("CocktailGalleryModel", back_populates="cocktail")
    reviews = relationship("ReviewCocktailModel", back_populates="cocktail")
    bar = relationship("BarModel", back_populates="cocktails")


class CocktailGalleryModel(Base):
    __tablename__ = "cocktails_gallery"

    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(200))
    cocktail_id: Mapped[int] = mapped_column(ForeignKey("cocktails.id"))

    cocktail = relationship("CocktailModel", back_populates="gallery")


class ReviewCocktailModel(Base):
    __tablename__ = "review_cocktail"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    rating: Mapped[float] = mapped_column(nullable=True)
    cocktail_id: Mapped[int] = mapped_column(ForeignKey("cocktails.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    cocktail = relationship("CocktailModel", back_populates="reviews")
    user = relationship("UserModel", back_populates="reviews_cocktail")
