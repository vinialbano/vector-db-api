from typing import Any, Dict, List, Optional

from fastapi import Depends
from pydantic import BaseModel

from app.api.documents.router import documents_router as router
from app.application.documents import (
    UpdateChunkCommand,
    UpdateChunkHandler,
)
from app.container import get_document_repository
from app.domain.documents.document_repository import DocumentRepository


def get_update_chunk_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> UpdateChunkHandler:
    """DI provider for UpdateChunkHandler"""
    return UpdateChunkHandler(document_repo)


class UpdateChunkRequest(BaseModel):
    text: Optional[str] = None
    embedding: Optional[List[float]] = None
    metadata: Optional[Dict[str, Any]] = None


class UpdateChunkResponse(BaseModel):
    document_id: str
    chunk_id: str

    class Config:
        from_attributes = True


@router.patch("/{document_id}/chunks/{chunk_id}", response_model=UpdateChunkResponse)
def update_chunk(
    document_id: str,
    chunk_id: str,
    request: UpdateChunkRequest,
    handler: UpdateChunkHandler = Depends(get_update_chunk_handler),
):
    """Update a chunk in a document."""
    command = UpdateChunkCommand(
        document_id=document_id,
        chunk_id=chunk_id,
        text=request.text,
        embedding=request.embedding,
        metadata=request.metadata,
    )
    response = handler.handle(command)
    return UpdateChunkResponse(
        document_id=response.document_id, chunk_id=response.chunk_id
    )
