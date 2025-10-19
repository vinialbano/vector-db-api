from fastapi import Depends
from pydantic import BaseModel, Field

from vector_db_api.application.commands.documents import (
    CreateDocumentCommand,
    CreateDocumentHandler,
)

from vector_db_api.presentation.container import get_create_document_handler
from vector_db_api.presentation.api.routers import documents_router as router


class CreateDocumentRequest(BaseModel):
    title: str = Field(
        ..., description="The title of the document", min_length=1, max_length=255
    )

    class Config:
        json_schema_extra = {
            "example": {
                "title": "My Document Title",
            }
        }


class CreateDocumentResponse(BaseModel):
    document_id: str = Field(..., description="The ID of the created document")

    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "123e4567-e89b-12d3-a456-426614174000",
            }
        }
        from_attributes = True


@router.post(
    "/",
    response_model=CreateDocumentResponse,
)
def create_document(
    request: CreateDocumentRequest,
    handler: CreateDocumentHandler = Depends(get_create_document_handler),
):
    """Create a new document."""
    command = CreateDocumentCommand(
        title=request.title,
    )
    result = handler.handle(command)
    return CreateDocumentResponse(
        document_id=result.document_id,
    )
