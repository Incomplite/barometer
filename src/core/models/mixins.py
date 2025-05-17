from datetime import datetime

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampModelMixin:
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
    )
