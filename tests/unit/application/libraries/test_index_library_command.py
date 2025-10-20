import pytest

from app.application.libraries import (
    IndexLibraryCommand,
    IndexLibraryHandler,
)
from app.domain.common import Embedding
from app.domain.documents import (
    Chunk,
    ChunkId,
    ChunkMetadata,
    Document,
    DocumentId,
    DocumentMetadata,
)
from app.domain.libraries import (
    BruteForceIndex,
    Library,
    LibraryId,
    LibraryMetadata,
)
from app.errors import NotFoundError
from app.infrastructure import InMemoryLibraryRepository


class FakeIndexer:
    def __init__(self):
        self.called_with = None

    def index(self, library: Library) -> None:
        self.called_with = library


def make_document_with_chunks():
    c = Chunk(
        id=ChunkId.generate(),
        text="t",
        embedding=Embedding.from_list([1.0, 0.0]),
        metadata=ChunkMetadata(source="s"),
    )
    doc = Document(
        id=DocumentId.generate(), chunks=[c], metadata=DocumentMetadata(title="T")
    )
    return doc


def test_handler_calls_indexer_and_returns_library_id():
    repo = InMemoryLibraryRepository()
    # create and persist a library with one document
    doc = make_document_with_chunks()
    doc_id = doc.id

    # create library and save it
    lib = Library(
        id=LibraryId.generate(),
        documents=[doc_id],
        metadata=LibraryMetadata(name="L", description="d"),
        vector_index=BruteForceIndex(),
    )
    repo.save(lib)

    fake_indexer = FakeIndexer()
    handler = IndexLibraryHandler(repo, fake_indexer)

    cmd = IndexLibraryCommand(library_id=str(lib.id))
    result = handler.handle(cmd)

    assert result is None
    assert fake_indexer.called_with is lib


def test_index_library_not_found():
    repo = InMemoryLibraryRepository()
    fake_indexer = FakeIndexer()
    handler = IndexLibraryHandler(repo, fake_indexer)

    cmd = IndexLibraryCommand(library_id=str(LibraryId.generate()))

    with pytest.raises(NotFoundError):
        handler.handle(cmd)
