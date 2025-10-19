from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from vector_db_api.domain.documents.document import Document
from vector_db_api.domain.documents.document_id import DocumentId


class DocumentRepository(ABC):
    """Repository contract for Document aggregates."""

    @abstractmethod
    def save(self, document: Document) -> None:
        raise NotImplementedError()

    @abstractmethod
    def find_by_id(self, document_id: DocumentId) -> Optional[Document]:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, document_id: DocumentId) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def exists(self, document_id: DocumentId) -> bool:
        raise NotImplementedError()
