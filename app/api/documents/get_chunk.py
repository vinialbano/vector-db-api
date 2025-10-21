from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.application.documents import GetChunkHandler, GetChunkQuery
from app.dependencies import get_document_repository
from app.domain.documents.document_repository import DocumentRepository

get_chunk_router = APIRouter()


def get_get_chunk_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> GetChunkHandler:
    return GetChunkHandler(document_repo)


class GetChunkResponse(BaseModel):
    chunk_id: str
    text: str
    embedding: List[float]
    metadata: Dict[str, Any]


@get_chunk_router.get(
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
