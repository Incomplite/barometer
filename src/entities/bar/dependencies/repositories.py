from typing import Annotated

from fastapi import Depends

from src.entities.bar.repositories import BarRepository

BarRepositoryDI = Annotated[BarRepository, Depends(BarRepository)]
