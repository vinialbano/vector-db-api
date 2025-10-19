from dataclasses import dataclass
from typing import Any, Dict, Optional

from app.domain.documents import DocumentId, DocumentRepository


@dataclass
class UpdateDocumentCommand:
    document_id: str
    title: Optional[str] = None
    author: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None


@dataclass
class UpdateDocumentResult:
    document_id: str


@dataclass
class UpdateDocumentHandler:
    _repository: DocumentRepository

    def handle(self, command: UpdateDocumentCommand) -> UpdateDocumentResult:
        doc_id = DocumentId.from_string(command.document_id)
        document = self._repository.find_by_id(doc_id)
        if document is None:
            raise ValueError(f"Document {command.document_id} not found")

        document.update_metadata(
            title=command.title,
            author=command.author,
            custom_fields=command.custom_fields,
        )
        self._repository.save(document)

        return UpdateDocumentResult(document_id=str(doc_id))
