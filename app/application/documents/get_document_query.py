from dataclasses import dataclass
from typing import Any, Dict, List

from app.domain.documents import DocumentId, DocumentRepository
from app.domain.documents.chunk import ChunkDict


@dataclass
class GetDocumentQuery:
    document_id: str


@dataclass
class GetDocumentResult:
    document_id: str
    chunk_count: int
    metadata: Dict[str, Any]
    chunks: List[ChunkDict]


@dataclass
class GetDocumentHandler:
    _repository: DocumentRepository

    def handle(self, query: GetDocumentQuery) -> GetDocumentResult:
        document_id = DocumentId.from_string(query.document_id)
        document = self._repository.find_by_id(document_id)
        if document is None:
            raise ValueError(f"Document {query.document_id} not found")

        # serialize document metadata
        metadata = {
            "title": document.metadata.title,
            "author": document.metadata.author,
            "created_at": document.metadata.created_at.isoformat(),
            "custom_fields": dict(document.metadata.custom_fields),
            "updated_at": document.metadata.updated_at.isoformat(),
        }

        # serialize chunks
        chunks_list: List[ChunkDict] = []
        for c in document.chunks:
            chunks_list.append(c.to_dict())

        return GetDocumentResult(
            document_id=str(document.id),
            chunk_count=document.chunk_count,
            metadata=metadata,
            chunks=chunks_list,
        )
