import pytest

from vector_db_api.domain.libraries import LibraryIndexerService
from vector_db_api.infrastructure.repositories import InMemoryDocumentRepository
from vector_db_api.domain.documents import (
    Chunk,
    ChunkId,
    ChunkMetadata,
    Document,
    DocumentId,
    DocumentMetadata,
    Embedding,
)


class FakeLibrary:
    def __init__(self, documents):
        self.documents = documents
        self.index_called_with = None

    def index(self, chunks):
        self.index_called_with = chunks


def make_document_with_chunks(num_chunks: int):
    chunks = []
    for i in range(num_chunks):
        chunks.append(
            Chunk(
                id=ChunkId.generate(),
                text=f"t{i}",
                embedding=Embedding.from_list([float(i), 0.0]),
                metadata=ChunkMetadata(source="s"),
            )
        )
    doc = Document(
        id=DocumentId.generate(), chunks=chunks, metadata=DocumentMetadata(title="T")
    )
    return doc


def test_indexer_service_aggregates_chunks_and_calls_library_index():
    repo = InMemoryDocumentRepository()

    # two documents with different numbers of chunks
    d1 = make_document_with_chunks(2)
    d2 = make_document_with_chunks(1)

    repo.save(d1)
    repo.save(d2)

    fake_lib = FakeLibrary(documents=[d1.id, d2.id])

    service = LibraryIndexerService(repo)
    service.index(fake_lib)

    # aggregated chunks should preserve order: d1.chunks then d2.chunks
    expected = d1.chunks + d2.chunks
    assert fake_lib.index_called_with == expected


def test_indexer_service_raises_if_document_missing():
    repo = InMemoryDocumentRepository()

    # only save one document
    d1 = make_document_with_chunks(1)
    repo.save(d1)

    # library references a non-existent document id
    missing_id = DocumentId.generate()
    fake_lib = FakeLibrary(documents=[d1.id, missing_id])

    service = LibraryIndexerService(repo)
    with pytest.raises(ValueError) as excinfo:
        service.index(fake_lib)

    assert str(missing_id) in str(excinfo.value)
