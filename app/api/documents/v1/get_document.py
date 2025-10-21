from typing import Any, Dict, List

from fastapi import Depends
from pydantic import BaseModel

from app.api.documents.router import documents_router as router
from app.application.documents import (
    GetDocumentHandler,
    GetDocumentQuery,
)
from app.dependencies import get_document_repository
from app.domain.documents.document_repository import DocumentRepository


def get_get_document_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> GetDocumentHandler:
    return GetDocumentHandler(document_repo)


class ChunkMetadataResponse(BaseModel):
    source: str
    page_number: int | None
    created_at: str
    custom_fields: Dict[str, Any]
    updated_at: str


class ChunkResponse(BaseModel):
    chunk_id: str
    text: str
    embedding: List[float]
    metadata: ChunkMetadataResponse


class DocumentMetadataResponse(BaseModel):
    title: str
    author: str | None
    created_at: str
    custom_fields: Dict[str, Any]
    updated_at: str


class GetDocumentResponse(BaseModel):
    document_id: str
    chunk_count: int
    metadata: DocumentMetadataResponse
    chunks: List[ChunkResponse]


@router.get("/{document_id}", response_model=GetDocumentResponse)
def get_document(
    document_id: str, handler: GetDocumentHandler = Depends(get_get_document_handler)
):
    query = GetDocumentQuery(document_id=document_id)
    result = handler.handle(query)
    return GetDocumentResponse(
        document_id=result.document_id,
        chunk_count=result.chunk_count,
        metadata=result.metadata,
        chunks=result.chunks,
    )
