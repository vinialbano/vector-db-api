from typing import Any, Dict, List, Optional

from fastapi import Depends, status
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


@router.patch(
    "/{document_id}/chunks/{chunk_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
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
    handler.handle(command)
