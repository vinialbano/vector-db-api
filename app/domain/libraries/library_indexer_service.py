from app.domain.documents import DocumentRepository
from app.domain.libraries import Library
from app.domain.libraries.indexed_chunk import IndexedChunk
from app.errors import NotFoundError


class LibraryIndexerService:
    """Indexes a library with the chunks from its documents"""

    _document_repository: DocumentRepository

    def __init__(self, document_repository: DocumentRepository):
        self._document_repository = document_repository

    def index(self, library: Library) -> None:
        """Load the library's documents, and index the collection of all the chunks they contain"""
        indexed_chunks = []
        for document_id in library.documents:
            document = self._document_repository.find_by_id(document_id)
            if not document:
                raise NotFoundError(f"Document {document_id} not found")
            for chunk in document.chunks:
                indexed_chunks.append(IndexedChunk.from_chunk(chunk, document_id))

        library.index(indexed_chunks)
