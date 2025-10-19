from typing import Any, Dict, Optional

from fastapi import Depends
from pydantic import BaseModel, ConfigDict

from app.api.libraries.router import libraries_router as router
from app.application.libraries import (
    UpdateLibraryCommand,
    UpdateLibraryHandler,
)
from app.container import get_library_repository
from app.domain.libraries import LibraryRepository


def get_update_library_handler(
    library_repo: LibraryRepository = Depends(get_library_repository),
) -> UpdateLibraryHandler:
    """DI provider for UpdateLibraryHandler"""
    return UpdateLibraryHandler(library_repo)


class UpdateLibraryRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None


class UpdateLibraryResponse(BaseModel):
    library_id: str
    model_config = ConfigDict(from_attributes=True)


@router.patch("/{library_id}", response_model=UpdateLibraryResponse)
def update_library(
    library_id: str,
    request: UpdateLibraryRequest,
    handler: UpdateLibraryHandler = Depends(get_update_library_handler),
):
    command = UpdateLibraryCommand(
        library_id=library_id,
        name=request.name,
        description=request.description,
        custom_fields=request.custom_fields,
    )
    response = handler.handle(command)
    return UpdateLibraryResponse(library_id=response.library_id)
