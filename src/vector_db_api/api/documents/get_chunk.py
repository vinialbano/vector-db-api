from fastapi import Depends
from pydantic import BaseModel

from vector_db_api.application.documents import GetChunkHandler, GetChunkQuery
from vector_db_api.api.routers import documents_router as router
from vector_db_api.container import get_get_chunk_handler


class GetChunkResponse(BaseModel):
    chunk_id: str
    text: str


@router.get(
    "/{document_id}/chunks/{chunk_id}",
    response_model=GetChunkResponse,
    tags=["documents", "chunks"],
)
def get_chunk(
    document_id: str,
    chunk_id: str,
    handler: GetChunkHandler = Depends(get_get_chunk_handler),
):
    query = GetChunkQuery(document_id=document_id, chunk_id=chunk_id)
    result = handler.handle(query)
    return GetChunkResponse(chunk_id=str(result.chunk.id), text=result.chunk.text)
