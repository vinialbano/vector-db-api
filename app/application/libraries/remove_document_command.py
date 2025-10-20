from dataclasses import dataclass

from app.domain.documents import DocumentId, DocumentRepository
from app.domain.libraries import LibraryId, LibraryRepository


@dataclass
class RemoveDocumentCommand:
    library_id: str
    document_id: str


@dataclass
class RemoveDocumentResult:
    removed: bool


@dataclass
class RemoveDocumentHandler:
    _library_repo: LibraryRepository
    _document_repo: DocumentRepository

    def handle(self, command: RemoveDocumentCommand) -> RemoveDocumentResult:
        library_id = LibraryId.from_string(command.library_id)
        document_id = DocumentId.from_string(command.document_id)

        library = self._library_repo.find_by_id(library_id)
        if library is None:
            raise ValueError(f"Library {command.library_id} not found")

        # Ensure document exists (domain may allow removing references even if document missing,
        # but our pattern checks existence first)
        exists = self._document_repo.exists(document_id)
        if not exists:
            raise ValueError(f"Document {command.document_id} not found")

        # Remove document reference from library (idempotent by library implementation)
        # Track whether it was removed by checking contains before/after
        was_present = library.contains_document(document_id)
        if not was_present:
            return RemoveDocumentResult(removed=False)
        library.remove_document(document_id)
        self._library_repo.save(library)

        return RemoveDocumentResult(removed=True)
