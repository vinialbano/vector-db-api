from fastapi import Depends
from pydantic import BaseModel

from vector_db_api.application.documents import (
    DeleteChunkCommand,
    DeleteChunkHandler,
)
from vector_db_api.api.routers import documents_router as router
from vector_db_api.container import get_delete_chunk_handler


class DeleteChunkResponse(BaseModel):
    document_id: str
    chunk_id: str

    class Config:
        from_attributes = True


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
