from dataclasses import dataclass
from typing import List

from app.domain.documents import ChunkId, DocumentId, DocumentRepository
from app.domain.documents.chunk import ChunkMetadataDict


@dataclass
class GetChunkQuery:
    document_id: str
    chunk_id: str


@dataclass
class GetChunkResult:
    chunk_id: str
    text: str
    embedding: List[float]
    metadata: ChunkMetadataDict


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
        chunk_dict = chunk.to_dict()

        return GetChunkResult(
            chunk_id=chunk_dict["chunk_id"],
            text=chunk_dict["text"],
            embedding=chunk_dict["embedding"],
            metadata=chunk_dict["metadata"],
        )
