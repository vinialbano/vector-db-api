from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from app.domain.documents import (
    Chunk,
    ChunkId,
    ChunkMetadata,
    Document,
    DocumentId,
    DocumentMetadata,
    DocumentRepository,
    Embedding,
)


@dataclass
class CreateDocumentCommand:
    title: str
    # chunks may be omitted when creating an empty document;
    # chunks can be added later via AddChunk command.
    chunks: Optional[List[Dict[str, Any]]] = (
        None  # each chunk: {text: str, embedding: List[float], metadata: Dict[str, Any]}
    )


@dataclass
class CreateDocumentResult:
    document_id: str


@dataclass
class CreateDocumentHandler:
    _repository: DocumentRepository

    def handle(self, command: CreateDocumentCommand) -> CreateDocumentResult:
        # build chunk entities if any were provided
        chunks: List[Chunk] = []
        if command.chunks:
            for c in command.chunks:
                chunk = Chunk(
                    id=ChunkId.generate(),
                    text=c["text"],
                    embedding=Embedding.from_list(c["embedding"]),
                    metadata=ChunkMetadata(
                        source=c.get("metadata", {}).get("source", "unknown"),
                        page_number=c.get("metadata", {}).get("page_number"),
                        custom_fields=c.get("metadata", {}),
                    ),
                )
                chunks.append(chunk)

        document = Document(
            id=DocumentId.generate(),
            chunks=chunks,
            metadata=DocumentMetadata(title=command.title),
        )

        self._repository.save(document)

        return CreateDocumentResult(document_id=str(document.id))
