from fastapi import Depends

from src.auth.dependencies.auth_module import CurrentUserRoleDI
from src.auth.exceptions import AdminRequiredException, UserRequiredException
from src.entities.user.models import UserRoleEnum


def admin_required(role: CurrentUserRoleDI):
    if role != UserRoleEnum.ADMIN:
        raise AdminRequiredException


def user_required(role: CurrentUserRoleDI):
    if role != UserRoleEnum.USER:
        raise UserRequiredException


AdminRequiredDI = Depends(admin_required)
UserRequiredDI = Depends(user_required)
