from vector_db_api.domain.documents import DocumentRepository
from vector_db_api.domain.libraries import Library


class LibraryIndexerService:
    """Indexes a library with the chunks from its documents"""

    _document_repository: DocumentRepository

    def __init__(self, document_repository: DocumentRepository):
        self._document_repository = document_repository

    def index(self, library: Library) -> None:
        """Load the library's documents, and index the collection of all the chunks they contain"""
        chunks = []
        for document_id in library.documents:
            document = self._document_repository.find_by_id(document_id)
            if not document:
                raise ValueError(f"Document {document_id} not found")
            chunks.extend([chunk for chunk in document.chunks])

        library.index(chunks)
