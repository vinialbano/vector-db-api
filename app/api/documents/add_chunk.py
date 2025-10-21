from typing import Dict, List

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict, Field

from app.application.documents import AddChunkCommand, AddChunkHandler
from app.dependencies import get_document_repository
from app.domain.documents import DocumentRepository

add_chunk_router = APIRouter()


def get_add_chunk_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> AddChunkHandler:
    """DI provider for AddChunkHandler"""
    return AddChunkHandler(document_repo)


class AddChunkRequest(BaseModel):
    class ChunkMetadataRequest(BaseModel):
        source: str | None = Field(None, description="Source of the chunk")
        page_number: int | None = Field(None, description="Optional page number")
        custom_fields: Dict[str, object] = Field(
            default_factory=dict, description="Optional custom metadata for the chunk"
        )

    text: str = Field(..., min_length=1)
    embedding: List[float]
    metadata: ChunkMetadataRequest = Field(default_factory=ChunkMetadataRequest)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "Chunk text",
                "embedding": [1.0, 0.0],
                "metadata": {"source": "upload"},
            }
        }
    )


class AddChunkResponse(BaseModel):
    chunk_id: str
    model_config = ConfigDict(from_attributes=True)


@add_chunk_router.post(
    "/{document_id}/chunks",
    status_code=status.HTTP_201_CREATED,
    response_model=AddChunkResponse,
)
def add_chunk(
    document_id: str,
    request: AddChunkRequest,
    handler: AddChunkHandler = Depends(get_add_chunk_handler),
):
    """Add a chunk to a document."""
    command = AddChunkCommand(
        document_id=document_id,
        text=request.text,
        embedding=request.embedding,
        metadata=request.metadata.model_dump(),
    )
    response = handler.handle(command)
    return AddChunkResponse.model_validate(response)
