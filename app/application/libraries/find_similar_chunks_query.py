from dataclasses import dataclass
from typing import Any, Dict, List

from app.domain.common import Embedding
from app.domain.documents.chunk_metadata import ChunkMetadataFilterDict
from app.domain.libraries import LibraryId, LibraryRepository
from app.domain.libraries.indexed_chunk import IndexedChunkDict
from app.errors import NotFoundError


@dataclass
class FindSimilarChunksQuery:
    library_id: str
    embedding: List[float]
    k: int = 5
    min_similarity: float = 0.0
    filters: ChunkMetadataFilterDict | None = None


class SimilarChunkDict(IndexedChunkDict):
    similarity: float


@dataclass
class FindSimilarChunksResult:
    library_id: str
    chunks: List[SimilarChunkDict]


@dataclass
class FindSimilarChunksHandler:
    _repository: LibraryRepository

    def handle(self, query: FindSimilarChunksQuery) -> FindSimilarChunksResult:
        lib_id = LibraryId.from_string(query.library_id)
        library = self._repository.find_by_id(lib_id)
        if library is None:
            raise NotFoundError(f"Library {query.library_id} not found")

        emb = Embedding.from_list(query.embedding)
        # Delegate to domain - let domain validation errors (e.g. index not built)
        # propagate to the application/API layer so callers receive a clear error.
        raw = library.find_similar_chunks(
            emb,
            query.k,
            query.filters,
            query.min_similarity,
        )

        chunks: List[SimilarChunkDict] = []
        for c, score in raw:
            chunks.append({**c.to_dict(), "similarity": score})

        return FindSimilarChunksResult(library_id=str(library.id), chunks=chunks)
