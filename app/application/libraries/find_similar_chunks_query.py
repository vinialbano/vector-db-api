from dataclasses import dataclass
from typing import List

from app.domain.documents import Embedding
from app.domain.documents.chunk import ChunkDict
from app.domain.libraries import LibraryId, LibraryRepository


@dataclass
class FindSimilarChunksQuery:
    library_id: str
    embedding: List[float]
    k: int = 5
    min_similarity: float = 0.0


@dataclass
class FindSimilarChunksResult:
    library_id: str
    chunks: List[ChunkDict]


@dataclass
class FindSimilarChunksHandler:
    _repository: LibraryRepository

    def handle(self, query: FindSimilarChunksQuery) -> FindSimilarChunksResult:
        lib_id = LibraryId.from_string(query.library_id)
        library = self._repository.find_by_id(lib_id)
        if library is None:
            raise ValueError(f"Library {query.library_id} not found")

        emb = Embedding.from_list(query.embedding)
        try:
            raw = library.find_similar_chunks(emb, query.k, query.min_similarity)
        except ValueError:
            # If index is not built or another domain error occurs, return empty list
            raw = []

        chunks: List[ChunkDict] = []
        for c in raw:
            chunks.append(c.to_dict())

        return FindSimilarChunksResult(library_id=str(library.id), chunks=chunks)
