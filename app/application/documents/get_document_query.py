from dataclasses import dataclass
from typing import Any, Dict, List

from app.domain.documents import DocumentId, DocumentRepository


@dataclass
class GetDocumentQuery:
    document_id: str


@dataclass
class GetDocumentResult:
    document_id: str
    chunk_count: int
    metadata: Dict[str, Any]
    chunks: List[Dict[str, Any]]


@dataclass
class GetDocumentHandler:
    _repository: DocumentRepository

    def handle(self, query: GetDocumentQuery) -> GetDocumentResult:
        doc_id = DocumentId.from_string(query.document_id)
        document = self._repository.find_by_id(doc_id)
        if document is None:
            raise ValueError(f"Document {query.document_id} not found")

        # serialize document metadata
        meta = {
            "title": document.metadata.title,
            "author": document.metadata.author,
            "created_at": document.metadata.created_at.isoformat(),
            "custom_fields": dict(document.metadata.custom_fields),
            "updated_at": document.metadata.updated_at.isoformat(),
        }

        # serialize chunks
        chunks_list: List[Dict[str, Any]] = []
        for c in document.chunks:
            chunk_meta = {
                "source": c.metadata.source,
                "page_number": c.metadata.page_number,
                "created_at": c.metadata.created_at.isoformat(),
                "custom_fields": dict(c.metadata.custom_fields),
                "updated_at": c.metadata.updated_at.isoformat(),
            }
            chunks_list.append(
                {
                    "chunk_id": str(c.id),
                    "text": c.text,
                    "embedding": list(c.embedding.values),
                    "metadata": chunk_meta,
                }
            )

        return GetDocumentResult(
            document_id=str(document.id),
            chunk_count=document.chunk_count,
            metadata=meta,
            chunks=chunks_list,
        )
