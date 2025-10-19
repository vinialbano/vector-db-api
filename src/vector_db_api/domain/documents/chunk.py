from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from vector_db_api.domain.common.decorators import refresh_timestamp_after
from vector_db_api.domain.documents.chunk_id import ChunkId
from vector_db_api.domain.documents.chunk_metadata import ChunkMetadata
from vector_db_api.domain.documents.embedding import Embedding


@dataclass
class Chunk:
    """Piece of text with embedding and metadata"""

    id: ChunkId
    text: str
    embedding: Embedding
    metadata: ChunkMetadata

    def __post_init__(self):
        if not self.text.strip():
            raise ValueError("Chunk text cannot be empty")

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
                raise ValueError("Chunk text cannot be empty")
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

    def similarity(self, embedding: Embedding) -> float:
        """Compute cosine similarity between this chunk's embedding and another embedding."""
        return self.embedding.cosine_similarity(embedding)

    def distance(self, embedding: Embedding) -> float:
        """Compute Euclidean distance between this chunk's embedding and another embedding."""
        return self.embedding.euclidean_distance(embedding)

    @property
    def dimension(self) -> int:
        """Return the dimensionality of this chunk's embedding."""
        return self.embedding.dimension
