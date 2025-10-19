from fastapi import Depends
from pydantic import BaseModel, ConfigDict

from app.api.libraries.router import libraries_router as router
from app.application.libraries import (
    DeleteLibraryCommand,
    DeleteLibraryHandler,
)
from app.container import get_library_repository
from app.domain.libraries import LibraryRepository


def get_delete_library_handler(
    library_repo: LibraryRepository = Depends(get_library_repository),
) -> DeleteLibraryHandler:
    """DI provider for DeleteLibraryHandler"""
    return DeleteLibraryHandler(library_repo)


class DeleteLibraryResponse(BaseModel):
    library_id: str
    deleted: bool

    model_config = ConfigDict(from_attributes=True)


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
