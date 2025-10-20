from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from app.domain.documents import ChunkId, DocumentId, DocumentRepository
from app.errors import NotFoundError


@dataclass
class UpdateChunkCommand:
    document_id: str
    chunk_id: str
    text: Optional[str] = None
    embedding: Optional[List[float]] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class UpdateChunkHandler:
    _repository: DocumentRepository

    def handle(self, command: UpdateChunkCommand) -> None:
        document_id = DocumentId.from_string(command.document_id)
        document = self._repository.find_by_id(document_id)
        if document is None:
            raise NotFoundError(f"Document {command.document_id} not found")

        chunk_id = ChunkId.from_string(command.chunk_id)

        # delegate update to domain
        document.update_chunk(
            chunk_id,
            text=command.text,
            embedding=command.embedding,
            metadata=command.metadata,
        )

        # persist
        self._repository.save(document)
