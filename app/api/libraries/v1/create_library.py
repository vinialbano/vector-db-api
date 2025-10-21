from typing import Dict
from uuid import UUID

from fastapi import Depends, status
from pydantic import BaseModel, ConfigDict, Field

from app.api.libraries.router import libraries_router as router
from app.application.libraries import (
    CreateLibraryCommand,
    CreateLibraryHandler,
)
from app.dependencies import (
    get_document_repository,
    get_library_repository,
    get_vector_index_factory,
)
from app.domain.documents import DocumentRepository
from app.domain.libraries import LibraryRepository, VectorIndex
from typing import Callable


def get_create_library_handler(
    library_repo: LibraryRepository = Depends(get_library_repository),
    document_repo: DocumentRepository = Depends(get_document_repository),
    vector_index_factory: Callable[[], VectorIndex] = Depends(get_vector_index_factory),
) -> CreateLibraryHandler:
    """DI provider for CreateLibraryHandler"""

    return CreateLibraryHandler(library_repo, document_repo, vector_index_factory)


class CreateLibraryRequest(BaseModel):
    class LibraryMetadataRequest(BaseModel):
        name: str | None = Field(None, description="Name of the library")
        description: str | None = Field(None, description="Description of the library")
        custom_fields: Dict[str, object] = Field(
            default_factory=dict, description="Optional custom metadata for the library"
        )

    metadata: LibraryMetadataRequest = Field(
        default_factory=LibraryMetadataRequest, description="Optional library metadata"
    )
    documents: list[UUID] = Field(
        default_factory=list,
        description="Optional list of document IDs (UUID) to add to the library on creation",
    )
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "documents": ["550e8400-e29b-41d4-a716-446655440000"],
                "metadata": {
                    "name": "My Library",
                    "description": "A description of my library",
                    "custom_fields": {"field1": "value1", "field2": "value2"},
                },
            }
        }
    )


class CreateLibraryResponse(BaseModel):
    library_id: str
    model_config = ConfigDict(from_attributes=True)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CreateLibraryResponse
)
def create_library(
    request: CreateLibraryRequest,
    handler: CreateLibraryHandler = Depends(get_create_library_handler),
):
    # Convert validated UUID objects to strings for the application layer
    command = CreateLibraryCommand(
        metadata=request.metadata.model_dump(),
        documents=[str(d) for d in request.documents],
    )
    response = handler.handle(command)
    return CreateLibraryResponse(library_id=response.library_id)
