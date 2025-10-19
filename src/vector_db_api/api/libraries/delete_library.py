from fastapi import Depends
from pydantic import BaseModel

from vector_db_api.api.routers import libraries_router as router
from vector_db_api.application.libraries import (
    DeleteLibraryCommand,
    DeleteLibraryHandler,
)
from vector_db_api.container import get_library_repository
from vector_db_api.domain.libraries import LibraryRepository


def get_delete_library_handler(
    library_repo: LibraryRepository = Depends(get_library_repository),
) -> DeleteLibraryHandler:
    """DI provider for DeleteLibraryHandler"""
    return DeleteLibraryHandler(library_repo)


class DeleteLibraryResponse(BaseModel):
    library_id: str
    deleted: bool

    class Config:
        from_attributes = True


@router.delete("/{library_id}", response_model=DeleteLibraryResponse)
def delete_library(
    library_id: str,
    handler: DeleteLibraryHandler = Depends(get_delete_library_handler),
):
    command = DeleteLibraryCommand(library_id=library_id)
    response = handler.handle(command)
    return DeleteLibraryResponse(
        library_id=response.library_id, deleted=response.deleted
    )
