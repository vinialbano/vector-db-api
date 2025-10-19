from dataclasses import dataclass

from app.domain.documents import DocumentId, ChunkId, DocumentRepository


@dataclass
class GetChunkQuery:
    document_id: str
    chunk_id: str


@dataclass
class GetChunkResult:
    chunk: object


@dataclass
class GetChunkHandler:
    _repository: DocumentRepository

    def handle(self, query: GetChunkQuery) -> GetChunkResult:
        doc_id = DocumentId.from_string(query.document_id)
        chunk_id = ChunkId.from_string(query.chunk_id)
        document = self._repository.find_by_id(doc_id)
        if document is None:
            raise ValueError(f"Document {query.document_id} not found")
        chunk = document.get_chunk(chunk_id)
        return GetChunkResult(chunk=chunk)
