from dataclasses import dataclass

from app.domain.documents import DocumentId, DocumentRepository


@dataclass
class GetDocumentQuery:
    document_id: str


@dataclass
class GetDocumentResult:
    document: object


@dataclass
class GetDocumentHandler:
    _repository: DocumentRepository

    def handle(self, query: GetDocumentQuery) -> GetDocumentResult:
        doc_id = DocumentId.from_string(query.document_id)
        document = self._repository.find_by_id(doc_id)
        if document is None:
            raise ValueError(f"Document {query.document_id} not found")
        return GetDocumentResult(document=document)
