from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict

from app.application.libraries import (
    DeleteLibraryCommand,
    DeleteLibraryHandler,
)
from app.dependencies import get_library_repository
from app.domain.libraries import LibraryRepository

delete_library_router = APIRouter()


def get_delete_library_handler(
    library_repo: LibraryRepository = Depends(get_library_repository),
) -> DeleteLibraryHandler:
    """DI provider for DeleteLibraryHandler"""
    return DeleteLibraryHandler(library_repo)


class DeleteLibraryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


@delete_library_router.delete(
    "/{library_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_library(
    library_id: str,
    handler: DeleteLibraryHandler = Depends(get_delete_library_handler),
):
    command = DeleteLibraryCommand(library_id=library_id)
    handler.handle(command)
    return None
