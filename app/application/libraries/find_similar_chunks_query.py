from dataclasses import dataclass
from typing import List

from app.domain.common import Embedding
from app.domain.libraries import LibraryId, LibraryRepository
from app.domain.libraries.indexed_chunk import IndexedChunkDict
from app.errors import NotFoundError


@dataclass
class FindSimilarChunksQuery:
    library_id: str
    embedding: List[float]
    k: int = 5
    min_similarity: float = 0.0


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
        from app.errors import InvalidEntityError

        try:
            raw = library.find_similar_chunks(emb, query.k, query.min_similarity)
        except InvalidEntityError:
            # If index is not built or another domain validation error occurs, return empty list
            raw = []

        chunks: List[SimilarChunkDict] = []
        for c, score in raw:
            chunks.append({**c.to_dict(), "similarity": score})

        return FindSimilarChunksResult(library_id=str(library.id), chunks=chunks)
