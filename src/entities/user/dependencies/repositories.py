from typing import Annotated

from fastapi import Depends

from src.entities.user.repositories import UserRepository

UserRepositoryDI = Annotated[UserRepository, Depends(UserRepository)]
