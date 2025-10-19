from fastapi import Depends
from pydantic import BaseModel, ConfigDict

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


class DeleteChunkResponse(BaseModel):
    document_id: str
    chunk_id: str

    model_config = ConfigDict(from_attributes=True)


@router.delete("/{document_id}/chunks/{chunk_id}", response_model=DeleteChunkResponse)
def delete_chunk(
    document_id: str,
    chunk_id: str,
    handler: DeleteChunkHandler = Depends(get_delete_chunk_handler),
):
    """Delete a chunk from a document."""
    command = DeleteChunkCommand(document_id=document_id, chunk_id=chunk_id)
    response = handler.handle(command)
    return DeleteChunkResponse(
        document_id=response.document_id, chunk_id=response.chunk_id
    )
