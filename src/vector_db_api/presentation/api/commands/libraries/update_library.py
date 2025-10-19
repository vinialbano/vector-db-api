from typing import Any, Dict, Optional

from fastapi import Depends
from pydantic import BaseModel

from vector_db_api.application.commands.libraries import (
    UpdateLibraryCommand,
    UpdateLibraryHandler,
)
from vector_db_api.presentation.api.routers import libraries_router as router
from vector_db_api.presentation.container import get_update_library_handler


class UpdateLibraryRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None


class UpdateLibraryResponse(BaseModel):
    library_id: str

    class Config:
        from_attributes = True


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
