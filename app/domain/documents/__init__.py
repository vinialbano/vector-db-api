"""Document aggregate public API."""

from app.domain.documents.chunk import Chunk
from app.domain.documents.chunk_id import ChunkId
from app.domain.documents.chunk_metadata import ChunkMetadata
from app.domain.documents.document import Document
from app.domain.documents.document_id import DocumentId
from app.domain.documents.document_metadata import DocumentMetadata
from app.domain.documents.document_repository import DocumentRepository

__all__ = [
    "Document",
    "DocumentId",
    "DocumentMetadata",
    "Chunk",
    "ChunkId",
    "ChunkMetadata",
    "DocumentRepository",
]
