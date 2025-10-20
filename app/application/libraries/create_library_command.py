from dataclasses import dataclass
from typing import Any, Callable, Dict, TypedDict

from app.domain.libraries import (
    Library,
    LibraryId,
    LibraryMetadata,
    LibraryRepository,
    VectorIndex,
)
from app.domain.documents import DocumentId, DocumentRepository


@dataclass
class CreateLibraryCommand:
    class LibraryMetadataInput(TypedDict):
        name: str
        description: str
        custom_fields: Dict[str, Any]

    metadata: LibraryMetadataInput
    # Optional list of document ids to add to the library during creation.
    documents: list[str] | None = None


@dataclass
class CreateLibraryResult:
    library_id: str


@dataclass
class CreateLibraryHandler:
    _repository: LibraryRepository
    _document_repository: DocumentRepository
    vector_index_factory: Callable[[], VectorIndex]

    def handle(self, command: CreateLibraryCommand) -> CreateLibraryResult:
        meta = command.metadata or {}
        name = meta.get("name")
        description = meta.get("description")
        custom_fields = meta.get("custom_fields", {}) or {}

        # Convert optionally provided document id strings into DocumentId objects
        doc_ids = []
        if getattr(command, "documents", None):
            for d in command.documents:
                document_id = DocumentId.from_string(d)
                if not self._document_repository.exists(document_id):
                    raise ValueError(f"Document {document_id} not found")
                doc_ids.append(document_id)

        vector_index = self.vector_index_factory()
        library = Library(
            id=LibraryId.generate(),
            documents=doc_ids,
            metadata=LibraryMetadata(
                name=name,
                description=description,
                custom_fields=custom_fields,
            ),
            vector_index=vector_index,
        )

        self._repository.save(library)

        return CreateLibraryResult(library_id=str(library.id))
