from dataclasses import dataclass

from app.domain.libraries import LibraryId, LibraryRepository
from app.domain.documents import DocumentId, DocumentRepository


@dataclass
class AddDocumentCommand:
    library_id: str
    document_id: str


@dataclass
class AddDocumentResult:
    library_id: str
    document_id: str


@dataclass
class AddDocumentHandler:
    _library_repo: LibraryRepository
    _document_repo: DocumentRepository

    def handle(self, command: AddDocumentCommand) -> AddDocumentResult:
        library_id = LibraryId.from_string(command.library_id)
        document_id = DocumentId.from_string(command.document_id)

        library = self._library_repo.find_by_id(library_id)
        if library is None:
            raise ValueError(f"Library {command.library_id} not found")

        document = self._document_repo.find_by_id(document_id)
        if document is None:
            raise ValueError(f"Document {command.document_id} not found")

        library.add_document(document_id)
        self._library_repo.save(library)

        return AddDocumentResult(
            library_id=str(library_id), document_id=str(document_id)
        )
