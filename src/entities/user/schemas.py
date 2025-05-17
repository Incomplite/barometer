from pydantic import Field

from src.core.schemas.base import BaseSchema
from src.entities.user.models import UserRoleEnum


class UserCreateSchema(BaseSchema):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4)
    role: UserRoleEnum = Field(default=UserRoleEnum.USER)


class UserUpdateSchema(BaseSchema):
    username: str | None = Field(None, min_length=3, max_length=50)
    password: str | None = Field(None, min_length=4)
    role: UserRoleEnum | None = Field(default=UserRoleEnum.USER)


class UserResponseSchema(BaseSchema):
    id: int
    username: str
    role: UserRoleEnum

    class Config:
        from_attributes = True
