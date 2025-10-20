import pytest

from app.domain.documents import DocumentId
from app.domain.libraries import (
    BruteForceIndex,
    IndexedChunk,
    Library,
    LibraryId,
    LibraryMetadata,
)


def test_library_creation(library_factory):
    lib = library_factory(documents=[])
    assert lib.metadata.name == "Library"
    assert lib.document_count == 0


def test_add_document_increments_and_invalidates(library_factory, document_factory):
    lib = library_factory(documents=[])
    # build an index using a sample document's chunks to mark library as indexed
    doc = document_factory()
    # convert document-owned chunks into IndexedChunk with document_id

    indexed = [IndexedChunk.from_chunk(c, doc.id) for c in doc.chunks]
    lib.index(indexed)
    assert lib.is_indexed
    lib.add_document(doc.id)

    assert lib.document_count == 1
    assert not lib.is_indexed


def test_add_duplicate_document_raises(library_factory, document_factory):
    lib = library_factory(documents=[])
    doc = document_factory()
    lib.add_document(doc.id)
    with pytest.raises(ValueError):
        lib.add_document(doc.id)


def test_remove_document_and_invalidate(library_factory, document_factory):
    doc = document_factory()
    lib = library_factory(documents=[doc])
    # create an index from the document's chunks so the library is indexed

    indexed = [IndexedChunk.from_chunk(c, doc.id) for c in doc.chunks]
    lib.index(indexed)
    assert lib.is_indexed

    lib.remove_document(doc.id)
    assert lib.document_count == 0
    assert not lib.is_indexed
    assert not lib.contains_document(doc.id)


def test_get_document_and_chunk_access(
    library_factory, document_factory, chunk_factory
):
    c1 = chunk_factory(text="a")
    c2 = chunk_factory(text="b")
    doc1 = document_factory(chunks=[c1])
    doc2 = document_factory(chunks=[c2])
    lib = library_factory(documents=[doc1, doc2])

    # library only stores references; ensure membership works
    assert lib.contains_document(doc1.id)

    # total_chunks is no longer a library responsibility; compute by loading documents
    all_chunks = doc1.chunks + doc2.chunks
    assert len(all_chunks) == 2
    assert c1 in all_chunks
    assert c2 in all_chunks


def test_updated_at_changes_on_invalidate(library_factory, document_factory):
    lib = library_factory(documents=[])
    before = lib.metadata.updated_at
    doc = document_factory()
    lib.add_document(doc.id)
    after = lib.metadata.updated_at
    assert after > before


def test_updated_at_changes_on_add_document(library_factory, document_factory):
    lib = library_factory(documents=[])
    before = lib.metadata.updated_at
    doc = document_factory()
    lib.add_document(doc.id)
    assert lib.metadata.updated_at > before


def test_updated_at_changes_on_remove_document(library_factory, document_factory):
    doc = document_factory()
    lib = library_factory(documents=[doc])
    before = lib.metadata.updated_at
    lib.remove_document(doc.id)
    assert lib.metadata.updated_at > before


def test_library_metadata_requires_name():
    # empty name should raise in metadata __post_init__
    with pytest.raises(ValueError):
        LibraryMetadata(name="", description="desc")


def test_library_requires_metadata():
    lid = LibraryId.generate()
    # None metadata should raise in Library.__post_init__
    with pytest.raises(ValueError):
        # pass a concrete index so constructor requirements are met
        Library(id=lid, documents=[], metadata=None, vector_index=BruteForceIndex())  # type: ignore


def test_index_builds_and_marks_indexed(library_factory, document_factory):
    # index() should build the index from provided chunks and set is_indexed
    lib = library_factory(documents=[])
    doc = document_factory()
    assert not lib.is_indexed

    indexed = [IndexedChunk.from_chunk(c, doc.id) for c in doc.chunks]
    lib.index(indexed)
    assert lib.is_indexed


def test_index_raises_on_empty_chunks(library_factory):
    lib = library_factory(documents=[])
    with pytest.raises(ValueError):
        lib.index([])


def test_index_raises_when_already_indexed(library_factory, document_factory):
    lib = library_factory(documents=[])
    doc = document_factory()

    indexed = [IndexedChunk.from_chunk(c, doc.id) for c in doc.chunks]
    lib.index(indexed)
    with pytest.raises(ValueError):
        lib.index(doc.chunks)


def test_invalidate_clears_underlying_index(library_factory, document_factory):
    lib = library_factory(documents=[])
    doc = document_factory()
    # After building index, underlying vector_index should have chunks

    indexed = [IndexedChunk.from_chunk(c, doc.id) for c in doc.chunks]
    lib.index(indexed)
    # assume the concrete index implementation exposes _chunks for inspection
    assert getattr(lib.vector_index, "_chunks", None) is not None
    lib.invalidate_index()
    assert not lib.is_indexed
    # concrete index clear() should have emptied stored chunks
    assert getattr(lib.vector_index, "_chunks", None) == []


def test_get_indexed_chunks_returns_chunks(chunk_factory, library_factory):
    # create a library with a brute-force index and index some chunks
    index = BruteForceIndex()
    lib = library_factory()
    lib.vector_index = index

    chunks = [chunk_factory(text=f"Chunk {i}") for i in range(3)]
    # index via library API — construct IndexedChunk with a dummy document id

    dummy_doc_id = DocumentId.generate()
    indexed = [IndexedChunk.from_chunk(c, dummy_doc_id) for c in chunks]
    lib.index(indexed)

    indexed = lib.get_indexed_chunks()
    assert isinstance(indexed, list)
    assert len(indexed) == 3
    assert indexed[0].text == chunks[0].text
