from src.auth.dependencies.services import AuthServiceDI
from src.entities.user.dependencies.repositories import UserRepositoryDI
from src.entities.user.exceptions import (
    InvalidInputError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.entities.user.schemas import (
    UserCreateSchema,
    UserResponseSchema,
    UserUpdateSchema,
)


class UserService:
    def __init__(
        self,
        user_repository: UserRepositoryDI,
        auth_service: AuthServiceDI,
    ) -> None:
        self._user_repository = user_repository
        self._auth_service = auth_service

    async def get_user_by_username(
        self,
        username: str,
    ) -> UserResponseSchema | None:
        if username is None:
            raise InvalidInputError
        user = await self._user_repository.get_user_by_username(username)
        return UserResponseSchema.model_validate(user) if user else None

    async def get_user_by_id(
        self,
        user_id: int,
    ) -> UserResponseSchema | None:
        user = await self._user_repository.get_user_by_id(user_id)
        return UserResponseSchema.model_validate(user)

    async def create_user(
        self,
        user: UserCreateSchema,
    ) -> UserResponseSchema:
        if await self._user_repository.get_user_by_username(user.username):
            raise UserAlreadyExistsError

        user.password = self._auth_service.get_password_hash(user.password)
        user_model = await self._user_repository.create_user(user)
        return UserResponseSchema.model_validate(user_model)

    async def update_user(
        self,
        user_id: int,
        user_data: UserUpdateSchema,
    ) -> UserResponseSchema:
        update_data = user_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        if "username" in update_data:
            try:
                existing_user = await self._user_repository.get_user_by_username(
                    update_data["username"]
                )
                if existing_user is not None and existing_user.id != user_id:
                    raise UserAlreadyExistsError
            except UserNotFoundError:
                pass

        if "password" in update_data:
            update_data["password"] = self._auth_service.get_password_hash(
                update_data["password"]
            )

        updated_user = await self._user_repository.update_user(
            user_id=user_id,
            update_data=update_data,
        )

        if updated_user is None:
            raise UserNotFoundError

        return UserResponseSchema.model_validate(updated_user)

    async def get_all_users(self) -> list[UserResponseSchema]:
        users = await self._user_repository.get_all_users()
        return [UserResponseSchema.model_validate(user) for user in users]

    async def delete_user(
        self,
        user_id: int,
    ) -> bool:
        return await self._user_repository.delete_user(user_id)
