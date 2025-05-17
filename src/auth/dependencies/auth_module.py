from typing import Annotated

from fastapi import Depends

from src.auth.utils import get_current_user, get_current_user_role
from src.entities.user.models import UserRoleEnum
from src.entities.user.schemas import UserResponseSchema

CurrentUserRoleDI = Annotated[UserRoleEnum, Depends(get_current_user_role)]
CurrentUserDI = Annotated[UserResponseSchema, Depends(get_current_user)]
