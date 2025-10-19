from fastapi import Depends
from pydantic import BaseModel

from app.api.documents.router import documents_router as router
from app.application.documents import (
    GetDocumentHandler,
    GetDocumentQuery,
)
from app.container import get_document_repository
from app.domain.documents.document_repository import DocumentRepository


def get_get_document_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> GetDocumentHandler:
    return GetDocumentHandler(document_repo)


class GetDocumentResponse(BaseModel):
    document_id: str


class GetChunkResponse(BaseModel):
    chunk_id: str
    text: str


@router.get("/{document_id}", response_model=GetDocumentResponse)
def get_document(
    document_id: str, handler: GetDocumentHandler = Depends(get_get_document_handler)
):
    query = GetDocumentQuery(document_id=document_id)
    result = handler.handle(query)
    return GetDocumentResponse(document_id=str(result.document.id))
