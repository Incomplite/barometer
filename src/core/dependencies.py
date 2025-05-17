from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_helpers import db_helper

DatabaseSessionDI = Annotated[AsyncSession, Depends(db_helper.get_db_session)]
