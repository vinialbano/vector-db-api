from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, List, Tuple

from app.domain.common.decorators import refresh_timestamp_after
from app.domain.documents import Chunk, DocumentId, Embedding
from app.domain.libraries.library_id import LibraryId
from app.domain.libraries.library_metadata import LibraryMetadata
from app.domain.libraries.vector_index import VectorIndex


def invalidate_index_after(fn: Callable) -> Callable:
    def wrapper(self: Library, *args, **kwargs) -> Any:
        result = fn(self, *args, **kwargs)
        # keep behavior: mark index invalid & refresh metadata
        self.invalidate_index()
        return result

    return wrapper


@dataclass
class Library:
    """Library Aggregate Root - stores references to documents (DocumentId).

    Documents themselves are separate aggregates; this Library keeps only
    DocumentId references and manages index state.
    """

    id: LibraryId
    documents: List[DocumentId]
    metadata: LibraryMetadata
    vector_index: VectorIndex
    _is_indexed: bool = field(default=False, init=False, repr=False)

    def __post_init__(self):
        if not self.metadata:
            raise ValueError("Library metadata cannot be empty")

    @invalidate_index_after
    def add_document(self, document_id: DocumentId) -> None:
        if any(d == document_id for d in self.documents):
            raise ValueError(
                f"Document {document_id} already exists in library {self.id}"
            )
        self.documents.append(document_id)

    @invalidate_index_after
    def remove_document(self, document_id: DocumentId) -> None:
        self.documents = [d for d in self.documents if d != document_id]

    @refresh_timestamp_after
    def index(self, chunks: List[Chunk]) -> None:
        """Build the vector index from the provided chunks"""
        if self.is_indexed:
            raise ValueError("Library is already indexed")
        if not chunks:
            raise ValueError("No chunks provided for indexing")
        self.vector_index.build(chunks)
        self._is_indexed = True

    @refresh_timestamp_after
    def invalidate_index(self) -> None:
        self._is_indexed = False
        self.vector_index.clear()

    @refresh_timestamp_after
    def update_metadata(
        self,
        *,
        name: str | None = None,
        description: str | None = None,
        custom_fields: dict | None = None,
    ) -> None:
        """Update library metadata using the value-object updated() factory."""
        self.metadata = self.metadata.updated(
            name=name, description=description, custom_fields=custom_fields
        )

    def _refresh_timestamp(self) -> None:
        """Refresh this library's metadata updated_at timestamp."""
        self.metadata = self.metadata.updated()

    def contains_document(self, document_id: DocumentId) -> bool:
        return any(d == document_id for d in self.documents)

    def find_similar_chunks(
        self,
        query_embedding: Embedding,
        k: int,
        min_similarity: float = 0.0,
    ) -> List[Tuple[Chunk, float]]:
        """Find the k most similar chunks to the given query embedding"""
        if k <= 0:
            raise ValueError("k must be a positive integer")
        results = self.vector_index.search(query_embedding, k)

        # Compute similarity and filter
        scored: List[Tuple[Chunk, float]] = []
        for chunk in results:
            score = chunk.similarity(query_embedding)
            if score >= min_similarity:
                scored.append((chunk, score))

        return scored

    def get_indexed_chunks(self) -> List[Chunk]:
        """Return all chunks currently indexed for this library."""
        return list(self.vector_index.get_chunks() or [])

    @property
    def is_indexed(self) -> bool:
        return self._is_indexed

    @property
    def document_count(self) -> int:
        return len(self.documents)

    @property
    def total_documents(self) -> int:
        return len(self.documents)
