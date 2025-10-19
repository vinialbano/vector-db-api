from typing import Any, Dict, List

from fastapi import Depends
from pydantic import BaseModel, Field

from app.api.documents.router import documents_router as router
from app.application.documents import AddChunkCommand, AddChunkHandler
from app.container import get_document_repository
from app.domain.documents import DocumentRepository


def get_add_chunk_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> AddChunkHandler:
    """DI provider for AddChunkHandler"""
    return AddChunkHandler(document_repo)


class AddChunkRequest(BaseModel):
    text: str = Field(..., min_length=1)
    embedding: List[float]
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Chunk text",
                "embedding": [1.0, 0.0],
                "metadata": {"source": "upload"},
            }
        }


class AddChunkResponse(BaseModel):
    chunk_id: str
    document_id: str

    class Config:
        from_attributes = True


@router.post("/{document_id}/chunks", response_model=AddChunkResponse)
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
        metadata=request.metadata,
    )
    response = handler.handle(command)
    return AddChunkResponse(
        chunk_id=response.chunk_id, document_id=response.document_id
    )
