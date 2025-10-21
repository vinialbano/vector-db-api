from fastapi import APIRouter, Depends, status

from app.application.documents import (
    DeleteChunkCommand,
    DeleteChunkHandler,
)
from app.dependencies import get_document_repository
from app.domain.documents import DocumentRepository

delete_chunk_router = APIRouter()


def get_delete_chunk_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> DeleteChunkHandler:
    """DI provider for DeleteChunkHandler"""
    return DeleteChunkHandler(document_repo)


@delete_chunk_router.delete(
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
