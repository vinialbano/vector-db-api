from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, TypedDict

from app.domain.common.embedding import Embedding
from app.domain.documents.chunk_id import ChunkId
from app.domain.documents.chunk_metadata import ChunkMetadata
from app.domain.documents.document_id import DocumentId


class ChunkMetadataDict(TypedDict):
    source: str
    page_number: int
    created_at: str
    updated_at: str
    custom_fields: Dict[str, Any]


class IndexedChunkDict(TypedDict):
    chunk_id: str
    document_id: str
    text: str
    embedding: List[float]
    metadata: ChunkMetadataDict


@dataclass(frozen=True)
class IndexedChunk:
    """Lightweight chunk representation used inside vector indexes."""

    id: ChunkId
    document_id: DocumentId
    text: str
    embedding: Embedding
    metadata: ChunkMetadata | None = None

    def similarity(self, other: Embedding) -> float:
        return self.embedding.cosine_similarity(other)

    def distance(self, other: Embedding) -> float:
        return self.embedding.euclidean_distance(other)

    def matches_filter(self, filters: Dict[str, Any]) -> bool:
        if self.metadata is None:
            return False
        return self.metadata.matches_filter(filters)

    @property
    def dimension(self) -> int:
        return self.embedding.dimension

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_id": str(self.id),
            "document_id": str(self.document_id),
            "text": self.text,
            "embedding": list(self.embedding.values),
            "metadata": {
                "source": self.metadata.source if self.metadata else None,
                "page_number": self.metadata.page_number if self.metadata else None,
                "created_at": self.metadata.created_at.isoformat()
                if self.metadata
                else None,
                "updated_at": self.metadata.updated_at.isoformat()
                if self.metadata
                else None,
                "custom_fields": dict(self.metadata.custom_fields)
                if self.metadata
                else {},
            },
        }

    @classmethod
    def from_chunk(cls, chunk, document_id: DocumentId) -> "IndexedChunk":
        """Create an IndexedChunk from a document-owned Chunk and its DocumentId."""
        return cls(
            id=chunk.id,
            document_id=document_id,
            text=chunk.text,
            embedding=chunk.embedding,
            metadata=getattr(chunk, "metadata", None),
        )
