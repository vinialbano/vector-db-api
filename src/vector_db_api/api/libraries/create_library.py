from fastapi import Depends
from pydantic import BaseModel

from vector_db_api.api.routers import libraries_router as router
from vector_db_api.application.libraries import (
    CreateLibraryCommand,
    CreateLibraryHandler,
)
from vector_db_api.container import get_library_repository
from vector_db_api.domain.libraries import KDTreeIndex, LibraryRepository


def get_create_library_handler(
    library_repo: LibraryRepository = Depends(get_library_repository),
) -> CreateLibraryHandler:
    """DI provider for CreateLibraryHandler"""
    return CreateLibraryHandler(library_repo, lambda: KDTreeIndex())


class CreateLibraryRequest(BaseModel):
    name: str
    description: str


class CreateLibraryResponse(BaseModel):
    library_id: str

    class Config:
        from_attributes = True


@router.post("/", response_model=CreateLibraryResponse)
def create_library(
    request: CreateLibraryRequest,
    handler: CreateLibraryHandler = Depends(get_create_library_handler),
):
    command = CreateLibraryCommand(name=request.name, description=request.description)
    response = handler.handle(command)
    return CreateLibraryResponse(library_id=response.library_id)
