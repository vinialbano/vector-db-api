from dataclasses import dataclass
from typing import Any, Dict, List, Optional, TypedDict

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
    class DocumentMetadataInput(TypedDict):
        title: str
        author: str
        custom_fields: Dict[str, Any]

    class ChunkInput(TypedDict):
        text: str
        embedding: List[float]

        class ChunkMetadataInput(TypedDict):
            source: str
            page_number: int
            custom_fields: Dict[str, Any]

        metadata: ChunkMetadataInput

    metadata: DocumentMetadataInput
    chunks: Optional[List[ChunkInput]] = None


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
                meta = c.get("metadata", {})
                chunk = Chunk(
                    id=ChunkId.generate(),
                    text=c["text"],
                    embedding=Embedding.from_list(c["embedding"]),
                    metadata=ChunkMetadata(
                        source=meta.get("source", "unknown"),
                        page_number=meta.get("page_number"),
                        custom_fields=meta.get("custom_fields", {}),
                    ),
                )
                chunks.append(chunk)

        # Extract document metadata required fields and custom fields
        meta = command.metadata or {}
        title = meta.get("title")
        author = meta.get("author")
        custom_fields = meta.get("custom_fields", {})

        document = Document(
            id=DocumentId.generate(),
            chunks=chunks,
            metadata=DocumentMetadata(
                title=title, author=author, custom_fields=custom_fields
            ),
        )

        self._repository.save(document)

        return CreateDocumentResult(document_id=str(document.id))
