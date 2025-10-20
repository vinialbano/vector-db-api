from dataclasses import dataclass

from app.domain.documents import DocumentId, DocumentRepository
from app.domain.libraries import LibraryId, LibraryRepository


@dataclass
class AddDocumentCommand:
    library_id: str
    document_id: str


@dataclass
class AddDocumentHandler:
    _library_repo: LibraryRepository
    _document_repo: DocumentRepository

    def handle(self, command: AddDocumentCommand) -> None:
        library_id = LibraryId.from_string(command.library_id)
        document_id = DocumentId.from_string(command.document_id)

        library = self._library_repo.find_by_id(library_id)
        if library is None:
            raise ValueError(f"Library {command.library_id} not found")

        if not self._document_repo.exists(document_id):
            raise ValueError(f"Document {command.document_id} not found")

        library.add_document(document_id)
        self._library_repo.save(library)
