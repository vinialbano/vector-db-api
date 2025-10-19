from dataclasses import dataclass

from vector_db_api.domain.documents import DocumentId, DocumentRepository


@dataclass
class DeleteDocumentCommand:
    document_id: str


@dataclass
class DeleteDocumentResult:
    id: str
    deleted: bool


@dataclass
class DeleteDocumentHandler:
    _repository: DocumentRepository

    def __init__(self, repository: DocumentRepository):
        self._repository = repository

    def handle(self, command: DeleteDocumentCommand) -> DeleteDocumentResult:
        document_id = DocumentId.from_string(command.document_id)
        deleted = self._repository.delete(document_id)
        return DeleteDocumentResult(id=str(document_id), deleted=deleted)
