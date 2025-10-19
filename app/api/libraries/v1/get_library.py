from fastapi import Depends
from pydantic import BaseModel

from app.api.libraries.router import libraries_router as router
from app.application.libraries import (
    GetLibraryHandler,
    GetLibraryQuery,
)
from app.container import get_library_repository
from app.domain.libraries.library_repository import LibraryRepository


def get_get_library_handler(
    library_repo: LibraryRepository = Depends(get_library_repository),
) -> GetLibraryHandler:
    return GetLibraryHandler(library_repo)


class LibraryResponse(BaseModel):
    library_id: str


@router.get("/{library_id}", response_model=LibraryResponse)
def get_library(
    library_id: str, handler: GetLibraryHandler = Depends(get_get_library_handler)
):
    query = GetLibraryQuery(library_id=library_id)
    result = handler.handle(query)
    return LibraryResponse(library_id=str(result.library.id))
