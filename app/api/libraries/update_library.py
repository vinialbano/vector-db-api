from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict

from app.application.libraries import (
    UpdateLibraryCommand,
    UpdateLibraryHandler,
)
from app.dependencies import get_library_repository
from app.domain.libraries import LibraryRepository

update_library_router = APIRouter()


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
    model_config = ConfigDict(from_attributes=True)


@update_library_router.patch(
    "/{library_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
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
    handler.handle(command)
    return None
