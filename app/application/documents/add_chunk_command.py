from dataclasses import dataclass
from typing import Any, Dict, List, NotRequired, TypedDict

from app.domain.common import Embedding
from app.domain.documents import (
    Chunk,
    ChunkId,
    ChunkMetadata,
    DocumentId,
    DocumentRepository,
)
from app.errors import NotFoundError


@dataclass
class AddChunkCommand:
    """Add a chunk to an existing document."""

    class ChunkMetadataInput(TypedDict):
        source: NotRequired[str]
        page_number: NotRequired[int]
        custom_fields: NotRequired[Dict[str, Any]]

    document_id: str
    text: str
    embedding: List[float]
    metadata: ChunkMetadataInput


@dataclass
class AddChunkResult:
    chunk_id: str


@dataclass
class AddChunkHandler:
    _document_repo: DocumentRepository

    def handle(self, command: AddChunkCommand) -> AddChunkResult:
        # Validate Document exists
        document_id = DocumentId.from_string(command.document_id)
        document = self._document_repo.find_by_id(document_id)
        if document is None:
            raise NotFoundError(f"Document {command.document_id} not found")

        # Create Chunk entity
        chunk_id = ChunkId.generate()
        chunk = Chunk(
            id=chunk_id,
            text=command.text,
            embedding=Embedding.from_list(command.embedding),
            metadata=ChunkMetadata(
                source=command.metadata.get("source", "unknown"),
                page_number=command.metadata.get("page_number"),
                custom_fields=command.metadata.get("custom_fields", {}),
            ),
        )

        # Add Chunk to Document aggregate
        document.add_chunk(chunk)
        self._document_repo.save(document)

        return AddChunkResult(chunk_id=str(chunk_id))
