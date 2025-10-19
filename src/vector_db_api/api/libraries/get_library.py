from fastapi import Depends
from pydantic import BaseModel

from vector_db_api.api.routers import libraries_router as router
from vector_db_api.application.libraries import (
    GetLibraryQuery,
    GetLibraryHandler,
)
from vector_db_api.container import get_get_library_handler


class LibraryResponse(BaseModel):
    library_id: str


@router.get("/{library_id}", response_model=LibraryResponse)
def get_library(
    library_id: str, handler: GetLibraryHandler = Depends(get_get_library_handler)
):
    query = GetLibraryQuery(library_id=library_id)
    result = handler.handle(query)
    return LibraryResponse(library_id=str(result.library.id))
