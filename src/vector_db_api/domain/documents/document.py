from __future__ import annotations

from dataclasses import dataclass
from typing import List

from vector_db_api.domain.common.decorators import refresh_timestamp_after

from .chunk import Chunk
from .chunk_id import ChunkId
from .document_id import DocumentId
from .document_metadata import DocumentMetadata


@dataclass
class Document:
    """Document entity - collection of chunks"""

    id: DocumentId
    chunks: List[Chunk]
    metadata: DocumentMetadata

    def __post_init__(self):
        # Documents are allowed to start with zero chunks. Chunks can be
        # added later via application commands (e.g. AddChunk).
        if self.chunks is None:
            self.chunks = []

    @refresh_timestamp_after
    def add_chunk(self, chunk: Chunk) -> None:
        if any(c.id == chunk.id for c in self.chunks):
            raise ValueError(f"Chunk {chunk.id} already exists in document")
        self.chunks.append(chunk)

    @refresh_timestamp_after
    def remove_chunk(self, chunk_id: ChunkId) -> None:
        self.chunks = [c for c in self.chunks if c.id != chunk_id]

    @refresh_timestamp_after
    def update_chunk(
        self,
        chunk_id: ChunkId,
        *,
        text: str | None = None,
        embedding: list | None = None,
        metadata: dict | None = None,
    ) -> None:
        """Find the chunk by id and delegate update to the Chunk entity.

        Raises ValueError if chunk not found.
        """
        for c in self.chunks:
            if c.id == chunk_id:
                c.update(text=text, embedding=embedding, metadata=metadata)
                return
        raise ValueError(f"Chunk {chunk_id} not found in document {self.id}")

    def update_metadata(
        self,
        *,
        title: str | None = None,
        author: str | None = None,
        custom_fields: dict | None = None,
    ) -> None:
        """Update document metadata in an immutable/value-object style.

        Only provided fields are updated; created_at is preserved.
        """
        self.metadata = self.metadata.updated(
            title=title, author=author, custom_fields=custom_fields
        )

    def _refresh_timestamp(self) -> None:
        """Refresh this document's metadata updated_at timestamp."""
        self.metadata = self.metadata.updated()

    @property
    def chunk_count(self) -> int:
        return len(self.chunks)

    def contains_chunk(self, chunk_id: ChunkId) -> bool:
        """Return True if this document contains a chunk with the given id."""
        return any(c.id == chunk_id for c in self.chunks)
