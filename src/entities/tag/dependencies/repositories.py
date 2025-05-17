from typing import Annotated

from fastapi import Depends

from src.entities.tag.repositories import TagRepository

TagRepositoryDI = Annotated[TagRepository, Depends(TagRepository)]
