import heapq
from dataclasses import dataclass, field
from typing import Any, Dict, List

from app.domain.common import Embedding
from app.domain.libraries.indexed_chunk import IndexedChunk
from app.domain.libraries.vector_index import VectorIndex
from app.errors import InvalidEntityError


@dataclass
class BruteForceIndex(VectorIndex):
    """
    Brute-force k-NN vector index implementation

    Time Complexity:
    - Build: O(1) - just stores the references
    - Search: O(n * d) where n is number of chunks and d is embedding dimension

    Space Complexity: O(n) - stores all chunks in memory

    Use case: Suitable for small datasets or testing purposes.
    """

    _chunks: List[IndexedChunk] = field(init=False, default_factory=list)

    def build(self, chunks: List[IndexedChunk]) -> None:
        if not chunks:
            raise InvalidEntityError("No chunks provided for indexing")

        # Validate all embeddings have the same dimension
        dimensions = {chunk.dimension for chunk in chunks}
        if len(dimensions) != 1:
            raise InvalidEntityError(
                "All chunks must have the same embedding dimension"
            )

        self._chunks = chunks

    def search(
        self, query: Embedding, k: int, filters: Dict[str, Any] | None = None
    ) -> List[IndexedChunk]:
        if not self._chunks:
            raise InvalidEntityError(
                "Index is empty. Build the index before searching."
            )

        if k <= 0:
            raise InvalidEntityError("k must be a positive integer")

        # Apply filters first
        candidates = self._chunks
        if filters:
            candidates = [c for c in candidates if c.matches_filter(filters)]

        if not candidates:
            return []

        # Compute similarity for all chunks.
        # Use an index as a tie-breaker so the heap never needs to
        # compare Chunk instances directly when similarities are equal.
        similarities: List[tuple[float, int, IndexedChunk]] = []
        for idx, chunk in enumerate(candidates):
            similarity = chunk.similarity(query)
            # Use negative similarity for min-heap (to get max values).
            # Tuple layout: ( -similarity, index, chunk )
            heapq.heappush(similarities, (-similarity, idx, chunk))

        # Get top-k chunks
        top_k = heapq.nsmallest(min(k, len(similarities)), similarities)
        return [chunk for _, _, chunk in top_k]

    def clear(self) -> None:
        """Clear the index"""
        self._chunks = []

    def get_chunks(self) -> List[IndexedChunk]:
        """Return the chunks stored in the index."""
        return list(self._chunks)
