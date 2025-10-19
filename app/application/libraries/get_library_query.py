from dataclasses import dataclass
from typing import Any, Dict, List

from app.domain.libraries import LibraryId, LibraryRepository


@dataclass
class GetLibraryQuery:
    library_id: str


@dataclass
class GetLibraryResult:
    library_id: str
    document_ids: List[str]
    metadata: Dict[str, Any]
    indexed_chunks: List[Dict[str, Any]]


@dataclass
class GetLibraryHandler:
    _repository: LibraryRepository

    def handle(self, query: GetLibraryQuery) -> GetLibraryResult:
        lib_id = LibraryId.from_string(query.library_id)
        library = self._repository.find_by_id(lib_id)
        if library is None:
            raise ValueError(f"Library {query.library_id} not found")

        # serialize metadata
        meta = {
            "name": library.metadata.name,
            "description": library.metadata.description,
            "created_at": library.metadata.created_at.isoformat(),
            "updated_at": library.metadata.updated_at.isoformat(),
            "custom_fields": dict(library.metadata.custom_fields),
        }

        # document ids as strings
        doc_ids = [str(d) for d in library.documents]

        # get indexed chunks via the Library public API
        raw_chunks = library.get_indexed_chunks()
        indexed_chunks: List[Dict[str, Any]] = []
        for c in raw_chunks:
            cm = {
                "source": c.metadata.source,
                "page_number": c.metadata.page_number,
                "created_at": c.metadata.created_at.isoformat(),
                "updated_at": c.metadata.updated_at.isoformat(),
                "custom_fields": dict(c.metadata.custom_fields),
            }
            indexed_chunks.append(
                {
                    "chunk_id": str(c.id),
                    "text": c.text,
                    "embedding": list(c.embedding.values),
                    "metadata": cm,
                }
            )

        return GetLibraryResult(
            library_id=str(library.id),
            document_ids=doc_ids,
            metadata=meta,
            indexed_chunks=indexed_chunks,
        )
