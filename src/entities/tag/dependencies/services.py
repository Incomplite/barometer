from typing import Annotated

from fastapi import Depends

from src.entities.tag.services import TagService

TagServiceDI = Annotated[TagService, Depends(TagService)]
