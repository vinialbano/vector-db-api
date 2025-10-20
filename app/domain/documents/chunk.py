from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, TypedDict

from app.domain.common.decorators import refresh_timestamp_after
from app.domain.common.embedding import Embedding
from app.domain.documents.chunk_id import ChunkId
from app.domain.documents.chunk_metadata import ChunkMetadata
from app.errors import InvalidEntityError


class ChunkMetadataDict(TypedDict):
    source: str
    page_number: int
    created_at: str
    updated_at: str
    custom_fields: Dict[str, Any]


class ChunkDict(TypedDict):
    chunk_id: str
    text: str
    embedding: List[float]
    metadata: ChunkMetadataDict


@dataclass
class Chunk:
    """Piece of text with embedding and metadata"""

    id: ChunkId
    text: str
    embedding: Embedding
    metadata: ChunkMetadata

    def __post_init__(self):
        if not self.text.strip():
            raise InvalidEntityError("Chunk text cannot be empty")

    def matches_filter(self, filters: Dict[str, Any]) -> bool:
        """Check if chunk matches metadata filters by delegating to metadata."""
        return self.metadata.matches_filter(filters)

    @refresh_timestamp_after
    def update(
        self,
        text: str | None = None,
        embedding: list | None = None,
        metadata: dict | None = None,
    ) -> None:
        """Update this chunk's fields using domain-validated methods.

        Only provided fields are updated. Validation mirrors constructor checks.
        """
        if text is not None:
            if not text.strip():
                raise InvalidEntityError("Chunk text cannot be empty")
            self.text = text

        if embedding is not None:
            self.embedding = Embedding.from_list(embedding)

        if metadata is not None:
            self.metadata = self.metadata.updated(
                source=metadata.get("source"),
                page_number=metadata.get("page_number"),
                custom_fields=metadata.get("custom_fields"),
            )

    def _refresh_timestamp(self) -> None:
        """Refresh the metadata's updated_at timestamp by creating a new metadata instance.

        This keeps metadata update semantics centralized in the value object.
        """
        self.metadata = self.metadata.updated()

    def to_dict(self) -> ChunkDict:
        """Serialize chunk to a dictionary with primitive types."""
        return {
            "chunk_id": str(self.id),
            "text": self.text,
            "embedding": list(self.embedding.values),
            "metadata": {
                "source": self.metadata.source,
                "page_number": self.metadata.page_number,
                "created_at": self.metadata.created_at.isoformat(),
                "updated_at": self.metadata.updated_at.isoformat(),
                "custom_fields": dict(self.metadata.custom_fields),
            },
        }
