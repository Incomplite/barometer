from enum import Enum

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db_helpers import Base


class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserModel(Base):
    __tablename__ = "users"
    __allow_unmapped__ = True

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )
    role: Mapped[UserRoleEnum] = mapped_column(
        nullable=False,
    )

    favorite_bars = relationship(
        "BarModel",
        secondary="user_favorite_bar_association",
        back_populates="favorited_by",
    )
    reviews_bar = relationship("ReviewBarModel", back_populates="user")
    reviews_cocktail = relationship("ReviewCocktailModel", back_populates="user")


class UserFavoriteBarAssociation(Base):
    __tablename__ = "user_favorite_bar_association"

    bar_id: Mapped[int] = mapped_column(
        ForeignKey("bars.id"),
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
