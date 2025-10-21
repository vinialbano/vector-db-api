import heapq
from dataclasses import dataclass
from typing import List, Optional

from app.domain.common import Embedding
from app.domain.documents.chunk_metadata import ChunkMetadataFilterDict
from app.domain.libraries.indexed_chunk import IndexedChunk
from app.domain.libraries.vector_index import VectorIndex
from app.errors import IndexNotBuiltError, InvalidEntityError


@dataclass
class KDNode:
    """Node in a KD-Tree"""

    chunk: IndexedChunk
    left: Optional["KDNode"] = None
    right: Optional["KDNode"] = None
    axis: int = 0  # Axis on which the node splits


@dataclass
class KDTreeIndex(VectorIndex):
    """

    KD-Tree for approximate nearest neighbor search in high-dimensional spaces.

    Time Complexity:
    - Build: O(n log n) where n is the number of chunks
    - Search: O(log n) average case, O(n) worst case

    Space Complexity: O(n) - stores all chunks in the tree

    Use case: Suitable for moderate-sized datasets where faster search is needed.
    Note: Performance degrades in very high dimensions due to the curse of dimensionality.
    """

    _root: Optional[KDNode] = None
    _dimension: int = 0

    def build(self, chunks: List[IndexedChunk]) -> None:
        if not chunks:
            raise InvalidEntityError("No chunks provided for indexing")

        # Validate all embeddings have the same dimension
        dimensions = {chunk.dimension for chunk in chunks}
        if len(dimensions) != 1:
            raise InvalidEntityError(
                "All chunks must have the same embedding dimension"
            )

        self._dimension = chunks[0].dimension
        self._root = self._build_tree(chunks, depth=0)

    def _build_tree(self, chunks: List[IndexedChunk], depth: int) -> Optional[KDNode]:
        if not chunks:
            return None

        # Select axis based on depth so that the tree is balanced
        axis = depth % self._dimension

        # Sort chunks by the selected axis
        sorted_chunks = sorted(chunks, key=lambda chunk: chunk.embedding.values[axis])

        # Select median as pivot element
        median_idx = len(sorted_chunks) // 2
        median_chunk = sorted_chunks[median_idx]

        # Recursively build subtrees
        return KDNode(
            chunk=median_chunk,
            left=self._build_tree(sorted_chunks[:median_idx], depth + 1),
            right=self._build_tree(sorted_chunks[median_idx + 1 :], depth + 1),
            axis=axis,
        )

    def search(
        self, query: Embedding, k: int, filters: ChunkMetadataFilterDict | None = None
    ) -> List[IndexedChunk]:
        if not self._root:
            raise IndexNotBuiltError(
                "Index is empty. Build the index before searching."
            )

        if k <= 0:
            raise InvalidEntityError("k must be a positive integer")
        # Use max-heap to track top-k nearest neighbors.
        # Include an index as a tie-breaker so the heap never needs
        # to compare IndexedChunk objects directly when distances are equal.
        neighbors: List[tuple[float, int, IndexedChunk]] = []
        _counter = 0

        def search_tree(
            node: Optional[KDNode],
            depth: int,
        ) -> None:
            if node is None:
                return

            # Check if node matches filters
            if filters and not node.chunk.matches_filter(filters):
                pass  # Continue searching tree but don't add this node
            else:
                # Compute distance
                distance = node.chunk.distance(query)
                nonlocal _counter
                if len(neighbors) < k:
                    heapq.heappush(neighbors, (-distance, _counter, node.chunk))
                    _counter += 1
                elif distance < -neighbors[0][0]:
                    # Replace the worst neighbor with the current one
                    heapq.heapreplace(neighbors, (-distance, _counter, node.chunk))
                    _counter += 1

            # Determine which branch to search next
            axis = depth % self._dimension
            diff = query.values[axis] - node.chunk.embedding.values[axis]

            if diff < 0:
                near_node, far_node = node.left, node.right
            else:
                near_node, far_node = node.right, node.left

            # Search nearer subtree first
            search_tree(near_node, depth + 1)

            # Check if we need to search the farther subtree
            if len(neighbors) < k or abs(diff) < -neighbors[0][0]:
                search_tree(far_node, depth + 1)

        search_tree(self._root, depth=0)
        # Return chunks ordered from nearest to farthest
        return [chunk for _, _, chunk in sorted(neighbors, key=lambda x: -x[0])]

    def clear(self) -> None:
        """Clear the index"""
        self._root = None
        self._dimension = 0

    def get_chunks(self) -> List[IndexedChunk]:
        """Return all chunks stored in the KD-tree via DFS traversal."""
        chunks: List[IndexedChunk] = []

        def dfs(node: Optional[KDNode]) -> None:
            if node is None:
                return
            chunks.append(node.chunk)
            dfs(node.left)
            dfs(node.right)

        dfs(self._root)
        return chunks
