from __future__ import annotations

from typing import Dict

from app.domain.documents import Document, DocumentId
from app.domain.documents.document_repository import DocumentRepository


class InMemoryDocumentRepository(DocumentRepository):
    def __init__(self):
        self._store: Dict[str, Document] = {}

    def save(self, document: Document) -> None:
        self._store[str(document.id)] = document

    def find_by_id(self, document_id: DocumentId) -> Document | None:
        return self._store.get(str(document_id))

    def delete(self, document_id: DocumentId) -> bool:
        return self._store.pop(str(document_id), None) is not None

    def exists(self, document_id: DocumentId) -> bool:
        return str(document_id) in self._store
