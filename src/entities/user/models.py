from enum import Enum

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

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
