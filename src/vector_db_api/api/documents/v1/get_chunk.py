from fastapi import Depends
from pydantic import BaseModel

from vector_db_api.api.documents.router import documents_router as router
from vector_db_api.application.documents import GetChunkHandler, GetChunkQuery
from vector_db_api.container import get_document_repository
from vector_db_api.domain.documents.document_repository import DocumentRepository


def get_get_chunk_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> GetChunkHandler:
    return GetChunkHandler(document_repo)


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
