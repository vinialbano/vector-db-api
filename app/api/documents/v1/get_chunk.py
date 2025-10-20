from typing import Any, Dict, List

from fastapi import Depends
from pydantic import BaseModel

from app.api.documents.router import documents_router as router
from app.application.documents import GetChunkHandler, GetChunkQuery
from app.container import get_document_repository
from app.domain.documents.document_repository import DocumentRepository


def get_get_chunk_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> GetChunkHandler:
    return GetChunkHandler(document_repo)


class GetChunkResponse(BaseModel):
    chunk_id: str
    text: str
    embedding: List[float]
    metadata: Dict[str, Any]


@router.get(
    "/{document_id}/chunks/{chunk_id}",
    response_model=GetChunkResponse,
)
def get_chunk(
    document_id: str,
    chunk_id: str,
    handler: GetChunkHandler = Depends(get_get_chunk_handler),
):
    query = GetChunkQuery(document_id=document_id, chunk_id=chunk_id)
    result = handler.handle(query)
    return GetChunkResponse(
        chunk_id=result.chunk_id,
        text=result.text,
        embedding=result.embedding,
        metadata=result.metadata,
    )
