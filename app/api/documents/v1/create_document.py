from typing import Any, Dict, List

from fastapi import Depends, status
from pydantic import BaseModel, ConfigDict, Field

from app.api.documents.router import documents_router as router
from app.application.documents import (
    CreateDocumentCommand,
    CreateDocumentHandler,
)
from app.container import get_document_repository
from app.domain.documents import DocumentRepository


def get_create_document_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),  # noqa: F821
) -> CreateDocumentHandler:
    """DI provider for CreateDocumentHandler"""
    return CreateDocumentHandler(document_repo)


class ChunkRequest(BaseModel):
    text: str = Field(..., description="Chunk text")
    embedding: List[float] = Field(..., description="Chunk embedding as list of floats")

    class ChunkMetadataRequest(BaseModel):
        source: str | None = Field(None, description="Source of the chunk")
        page_number: int | None = Field(None, description="Optional page number")
        custom_fields: Dict[str, object] = Field(
            default_factory=dict, description="Optional custom metadata for the chunk"
        )

    metadata: ChunkMetadataRequest = Field(
        default_factory=ChunkMetadataRequest, description="Optional chunk metadata"
    )


class CreateDocumentRequest(BaseModel):
    class DocumentMetadataRequest(BaseModel):
        title: str = Field(
            ..., description="The title of the document", min_length=1, max_length=255
        )
        author: str | None = Field(None, description="Author of the document")
        custom_fields: Dict[str, Any] | None = Field(
            None, description="Optional custom metadata for the document"
        )

    metadata: DocumentMetadataRequest

    chunks: list[ChunkRequest] | None = Field(
        None, description="Optional list of chunks to include in the document"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "metadata": {
                        "title": "My Document Title",
                        "author": "Jane Doe",
                        "custom_fields": {"category": "reports", "source": "scanner"},
                    },
                    "chunks": [
                        {
                            "text": "First chunk text",
                            "embedding": [0.1, 0.2, 0.3],
                            "metadata": {"source": "upload", "page_number": 1},
                        },
                        {
                            "text": "Second chunk text",
                            "embedding": [0.4, 0.5, 0.6],
                            "metadata": {"source": "upload", "page_number": 2},
                        },
                    ],
                },
                {
                    "metadata": {
                        "title": "My Document Title",
                        "author": "Jane Doe",
                        "custom_fields": {"category": "reports", "source": "scanner"},
                    },
                },
            ]
        }
    )


class CreateDocumentResponse(BaseModel):
    document_id: str = Field(..., description="The ID of the created document")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "document_id": "123e4567-e89b-12d3-a456-426614174000",
            }
        },
        from_attributes=True,
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateDocumentResponse,
)
def create_document(
    request: CreateDocumentRequest,
    handler: CreateDocumentHandler = Depends(get_create_document_handler),
):
    """Create a new document."""
    command = CreateDocumentCommand(
        metadata=request.metadata.model_dump(),
        chunks=[c.model_dump() for c in request.chunks] if request.chunks else None,
    )
    result = handler.handle(command)
    return CreateDocumentResponse.model_validate(result)
