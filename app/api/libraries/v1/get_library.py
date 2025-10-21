from typing import Any, Dict, List

from fastapi import Depends
from pydantic import BaseModel

from app.api.libraries.router import libraries_router as router
from app.application.libraries import (
    GetLibraryHandler,
    GetLibraryQuery,
)
from app.dependencies import get_library_repository
from app.domain.libraries.library_repository import LibraryRepository


def get_get_library_handler(
    library_repo: LibraryRepository = Depends(get_library_repository),
) -> GetLibraryHandler:
    return GetLibraryHandler(library_repo)


class ChunkMetadataResponse(BaseModel):
    source: str
    page_number: int | None
    created_at: str
    updated_at: str
    custom_fields: Dict[str, Any]


class ChunkResponse(BaseModel):
    chunk_id: str
    text: str
    embedding: List[float]
    metadata: ChunkMetadataResponse


class LibraryMetadataResponse(BaseModel):
    name: str
    description: str
    created_at: str
    updated_at: str
    custom_fields: Dict[str, Any]


class LibraryResponse(BaseModel):
    library_id: str
    document_ids: List[str]
    metadata: LibraryMetadataResponse
    indexed_chunks: List[ChunkResponse]


@router.get("/{library_id}", response_model=LibraryResponse)
def get_library(
    library_id: str, handler: GetLibraryHandler = Depends(get_get_library_handler)
):
    query = GetLibraryQuery(library_id=library_id)
    result = handler.handle(query)
    return LibraryResponse(
        library_id=result.library_id,
        document_ids=result.document_ids,
        metadata=result.metadata,
        indexed_chunks=result.indexed_chunks,
    )
