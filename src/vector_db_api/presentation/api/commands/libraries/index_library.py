from fastapi import Depends
from pydantic import BaseModel

from vector_db_api.application.commands.libraries import (
    IndexLibraryCommand,
    IndexLibraryHandler,
)
from vector_db_api.presentation.api.routers import libraries_router as router
from vector_db_api.presentation.container import get_index_library_handler


class IndexLibraryResponse(BaseModel):
    library_id: str

    class Config:
        from_attributes = True


@router.post("/{library_id}/index", response_model=IndexLibraryResponse)
def index_library(
    library_id: str,
    handler: IndexLibraryHandler = Depends(get_index_library_handler),
):
    command = IndexLibraryCommand(library_id=library_id)
    response = handler.handle(command)
    return IndexLibraryResponse(library_id=response.library_id)
