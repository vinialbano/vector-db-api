from dataclasses import dataclass

from app.domain.documents import DocumentId, DocumentRepository


@dataclass
class DeleteDocumentCommand:
    document_id: str


@dataclass
class DeleteDocumentHandler:
    _repository: DocumentRepository

    def __init__(self, repository: DocumentRepository):
        self._repository = repository

    def handle(self, command: DeleteDocumentCommand) -> None:
        document_id = DocumentId.from_string(command.document_id)
        self._repository.delete(document_id)
