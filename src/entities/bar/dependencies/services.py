from typing import Annotated

from fastapi import Depends

from src.entities.bar.services import BarService

BarServiceDI = Annotated[BarService, Depends(BarService)]
