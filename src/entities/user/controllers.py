from fastapi import APIRouter, Depends

from src.auth.dependencies.auth_module import CurrentUserDI
from src.auth.role_checks import admin_required
from src.config import project_config
from src.entities.user.dependencies.services import UserServiceDI
from src.entities.user.exceptions import (
    UserAlreadyExistsError,
    UserAlreadyExistsException,
    UserNotFoundError,
    UserNotFoundException,
)
from src.entities.user.models import UserRoleEnum
from src.entities.user.schemas import (
    UserCreateSchema,
    UserResponseSchema,
    UserUpdateSchema,
)

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@user_router.post(
    "/",
    response_model=UserResponseSchema,
    dependencies=[
        Depends(admin_required),
    ],
)
async def create_user(
    service: UserServiceDI,
    user_data: UserCreateSchema,
):
    try:
        user = await service.create_user(user_data)
        return user
    except UserAlreadyExistsError:
        raise UserAlreadyExistsException


@user_router.get(
    "/me",
    response_model=UserResponseSchema,
)
async def get_me(user: CurrentUserDI):
    return user


@user_router.post(
    "/createAdmin",
)
async def create_admin_user(service: UserServiceDI):
    admin_user = await service.get_user_by_username(
        project_config.auth.INITIAL_ADMIN_USERNAME
    )
    if not admin_user:
        await service.create_user(
            UserCreateSchema(
                username=project_config.auth.INITIAL_ADMIN_USERNAME,
                password=project_config.auth.INITIAL_ADMIN_PASSWORD,
                role=UserRoleEnum.ADMIN,
            )
        )
    return {
        "message": "Admin created successfully",
    }


@user_router.get(
    "/",
    response_model=list[UserResponseSchema],
    dependencies=[
        Depends(admin_required),
    ],
)
async def get_users(service: UserServiceDI):
    return await service.get_all_users()


@user_router.patch(
    "/{user_id}",
    response_model=UserResponseSchema,
    dependencies=[
        Depends(admin_required),
    ],
)
async def update_user(
    service: UserServiceDI,
    user_id: int,
    user_data: UserUpdateSchema,
):
    try:
        user = await service.update_user(
            user_id=user_id,
            user_data=user_data,
        )
    except UserAlreadyExistsError:
        raise UserAlreadyExistsException
    except UserNotFoundError:
        raise UserNotFoundException
    return user


@user_router.delete(
    "/{user_id}",
    dependencies=[
        Depends(admin_required),
    ],
)
async def delete_user(
    service: UserServiceDI,
    user_id: int,
):
    user = await service.delete_user(
        user_id=user_id,
    )
    if not user:
        raise UserNotFoundException
    return {
        "message": "User deleted successfully",
    }
