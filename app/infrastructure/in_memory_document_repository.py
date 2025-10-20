from __future__ import annotations

from typing import Dict
from threading import RLock

from app.domain.documents import Document, DocumentId
from app.domain.documents.document_repository import DocumentRepository
from app.errors import NotFoundError


class InMemoryDocumentRepository(DocumentRepository):
    def __init__(self):
        self._store: Dict[str, Document] = {}
        self._lock = RLock()

    def save(self, document: Document) -> None:
        with self._lock:
            self._store[str(document.id)] = document

    def find_by_id(self, document_id: DocumentId) -> Document | None:
        with self._lock:
            return self._store.get(str(document_id))

    def delete(self, document_id: DocumentId) -> None:
        with self._lock:
            removed = self._store.pop(str(document_id), None)
        if removed is None:
            raise NotFoundError(f"Document {document_id} not found")

    def exists(self, document_id: DocumentId) -> bool:
        with self._lock:
            return str(document_id) in self._store

    def clear(self) -> None:
        """Clear all stored documents (thread-safe)."""
        with self._lock:
            self._store.clear()
