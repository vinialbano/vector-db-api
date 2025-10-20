from fastapi import Depends, status

from app.api.documents.router import documents_router as router
from app.application.documents import (
    DeleteChunkCommand,
    DeleteChunkHandler,
)
from app.container import get_document_repository
from app.domain.documents import DocumentRepository


def get_delete_chunk_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> DeleteChunkHandler:
    """DI provider for DeleteChunkHandler"""
    return DeleteChunkHandler(document_repo)


@router.delete(
    "/{document_id}/chunks/{chunk_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_chunk(
    document_id: str,
    chunk_id: str,
    handler: DeleteChunkHandler = Depends(get_delete_chunk_handler),
):
    """Delete a chunk from a document."""
    command = DeleteChunkCommand(document_id=document_id, chunk_id=chunk_id)
    handler.handle(command)
