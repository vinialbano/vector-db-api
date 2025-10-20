from dataclasses import dataclass
from typing import Any, Dict, List

from app.domain.documents import ChunkId, DocumentId, DocumentRepository


@dataclass
class GetChunkQuery:
    document_id: str
    chunk_id: str


@dataclass
class GetChunkResult:
    chunk_id: str
    text: str
    embedding: List[float]
    metadata: Dict[str, Any]


@dataclass
class GetChunkHandler:
    _repository: DocumentRepository

    def handle(self, query: GetChunkQuery) -> GetChunkResult:
        document_id = DocumentId.from_string(query.document_id)
        chunk_id = ChunkId.from_string(query.chunk_id)
        document = self._repository.find_by_id(document_id)
        if document is None:
            raise ValueError(f"Document {query.document_id} not found")
        chunk = document.get_chunk(chunk_id)
        # serialize embedding to list of floats
        embedding_list = list(chunk.embedding.values)
        # serialize metadata to primitives (isoformat for datetimes)
        metadata = {
            "source": chunk.metadata.source,
            "page_number": chunk.metadata.page_number,
            "created_at": chunk.metadata.created_at.isoformat(),
            "updated_at": chunk.metadata.updated_at.isoformat(),
            "custom_fields": dict(chunk.metadata.custom_fields),
        }
        return GetChunkResult(
            chunk_id=str(chunk.id),
            text=chunk.text,
            embedding=embedding_list,
            metadata=metadata,
        )
