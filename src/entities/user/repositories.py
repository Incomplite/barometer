from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import DatabaseSessionDI
from src.entities.user.exceptions import UserNotFoundError
from src.entities.user.models import UserModel
from src.entities.user.schemas import UserCreateSchema


class UserRepository:
    model = UserModel

    def __init__(self, db_session: DatabaseSessionDI) -> None:
        self._session: AsyncSession = db_session

    async def get_user_by_username(
        self,
        username: str,
    ) -> UserModel | None:
        query = select(self.model).where(self.model.username == username)
        return await self._session.scalar(query)

    async def get_user_by_id(
        self,
        user_id: int,
    ) -> UserModel:
        query = select(self.model).where(self.model.id == user_id)
        user = await self._session.scalar(query)
        if user is None:
            raise UserNotFoundError
        return user

    async def get_all_users(self) -> Sequence[UserModel]:
        query = select(self.model)
        results = await self._session.scalars(query)
        return results.all()

    async def create_user(
        self,
        user: UserCreateSchema,
    ) -> UserModel:
        user_model = self.model(**user.model_dump())
        self._session.add(user_model)
        await self._session.commit()
        return user_model

    async def update_user(
        self,
        user_id: int,
        update_data: dict[str, Any],
    ) -> UserModel | None:
        user = await self._session.get(self.model, user_id)
        if user is not None:
            for key, value in update_data.items():
                setattr(user, key, value)

            await self._session.commit()
            await self._session.refresh(user)
        return user

    async def delete_user(
        self,
        user_id: int,
    ) -> bool:
        user = await self._session.get(self.model, user_id)
        if user is not None:
            await self._session.delete(user)
            await self._session.commit()
            return True
        return False
