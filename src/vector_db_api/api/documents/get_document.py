from fastapi import Depends
from pydantic import BaseModel

from vector_db_api.application.documents import (
    GetDocumentHandler,
    GetDocumentQuery,
)
from vector_db_api.api.routers import documents_router as router
from vector_db_api.container import get_get_document_handler


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
