from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.application.libraries.find_similar_chunks_query import (
    FindSimilarChunksHandler,
    FindSimilarChunksQuery,
)
from app.dependencies import get_library_repository
from app.domain.documents.chunk_metadata import ChunkMetadataFilterDict
from app.domain.libraries.library_repository import LibraryRepository

find_similar_chunks_router = APIRouter()


def get_find_similar_chunks_handler(
    library_repo: LibraryRepository = Depends(get_library_repository),
) -> FindSimilarChunksHandler:
    return FindSimilarChunksHandler(library_repo)


class ChunkMetadataResponse(BaseModel):
    source: str
    page_number: int | None
    created_at: str
    updated_at: str
    custom_fields: Dict[str, Any]


class ChunkResponse(BaseModel):
    chunk_id: str
    document_id: str
    similarity: float
    text: str
    embedding: List[float]
    metadata: ChunkMetadataResponse


class FindSimilarRequest(BaseModel):
    embedding: List[float]
    k: int = 5
    min_similarity: float = 0.0
    filters: ChunkMetadataFilterDict | None = None


class FindSimilarResponse(BaseModel):
    library_id: str
    chunks: List[ChunkResponse]


@find_similar_chunks_router.post(
    "/{library_id}/find-similar",
    response_model=FindSimilarResponse,
)
def find_similar_chunks(
    library_id: str,
    req: FindSimilarRequest,
    handler: FindSimilarChunksHandler = Depends(get_find_similar_chunks_handler),
):
    query = FindSimilarChunksQuery(
        library_id=library_id,
        embedding=req.embedding,
        k=req.k,
        min_similarity=req.min_similarity,
        filters=req.filters,
    )
    res = handler.handle(query)
    return FindSimilarResponse(library_id=res.library_id, chunks=res.chunks)
