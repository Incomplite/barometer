from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db_helpers import Base


class TagModel(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    bars = relationship(
        "BarModel",
        secondary="bar_and_tag_association",
        back_populates="tags",
    )


class BarAndTagAssociation(Base):
    __tablename__ = "bar_and_tag_association"

    bar_id: Mapped[int] = mapped_column(
        ForeignKey("bars.id"),
        primary_key=True,
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id"),
        primary_key=True,
    )
