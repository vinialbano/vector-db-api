from dataclasses import dataclass
from typing import List, TypedDict, NotRequired

from app.domain.documents import (
    Chunk,
    ChunkId,
    ChunkMetadata,
    DocumentId,
    DocumentRepository,
    Embedding,
)


@dataclass
class AddChunkCommand:
    """Add a chunk to an existing document.

    The client must provide `document_id` — documents must be created explicitly
    before chunks are added.
    """

    document_id: str
    text: str
    embedding: List[float]

    # Strongly-typed dict shape for chunk metadata received from clients.
    # Use NotRequired for optional keys so callers don't have to pass every field.
    class ChunkMetadataDict(TypedDict):
        source: NotRequired[str]
        page_number: NotRequired[int]
        # allow arbitrary extra keys for extensibility
        # (these will be forwarded into ChunkMetadata.custom_fields)
        # clients may include any additional fields as needed
        # Example: {"source": "upload", "page_number": 3, "lang": "en"}

    metadata: ChunkMetadataDict


@dataclass
class AddChunkResult:
    chunk_id: str
    document_id: str


@dataclass
class AddChunkHandler:
    _document_repo: DocumentRepository

    def handle(self, command: AddChunkCommand) -> AddChunkResult:
        # Validate Document exists
        document_id = DocumentId.from_string(command.document_id)
        document = self._document_repo.find_by_id(document_id)
        if document is None:
            raise ValueError(f"Document {command.document_id} not found")

        # Create Chunk entity
        chunk_id = ChunkId.generate()
        chunk = Chunk(
            id=chunk_id,
            text=command.text,
            embedding=Embedding.from_list(command.embedding),
            metadata=ChunkMetadata(
                source=command.metadata.get("source", "unknown"),
                page_number=command.metadata.get("page_number"),
                custom_fields=command.metadata,
            ),
        )

        # Add Chunk to Document aggregate
        document.add_chunk(chunk)
        self._document_repo.save(document)

        return AddChunkResult(chunk_id=str(chunk_id), document_id=str(document_id))
