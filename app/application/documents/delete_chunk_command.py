from dataclasses import dataclass

from app.domain.documents import ChunkId, DocumentId, DocumentRepository


@dataclass
class DeleteChunkCommand:
    document_id: str
    chunk_id: str


@dataclass
class DeleteChunkHandler:
    _repository: DocumentRepository

    def handle(self, command: DeleteChunkCommand) -> None:
        document_id = DocumentId.from_string(command.document_id)
        document = self._repository.find_by_id(document_id)
        if document is None:
            raise ValueError(f"Document {command.document_id} not found")

        chunk_id = ChunkId.from_string(command.chunk_id)
        if not document.contains_chunk(chunk_id):
            raise ValueError(
                f"Chunk {command.chunk_id} not found in document {command.document_id}"
            )

        document.remove_chunk(chunk_id)
        self._repository.save(document)
