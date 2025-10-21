from app.api.libraries.find_similar_chunks import (
    FindSimilarRequest,
    find_similar_chunks,
)
from app.application.libraries import FindSimilarChunksHandler
from app.domain.libraries.indexed_chunk import IndexedChunk
from app.infrastructure import InMemoryLibraryRepository


def test_find_similar_chunks_presentation(library_factory, document_factory):
    repo = InMemoryLibraryRepository()
    lib = library_factory()
    # ensure there is an indexed chunk available for the search
    if not lib.get_indexed_chunks():
        d = document_factory()
        indexed = [IndexedChunk.from_chunk(c, d.id) for c in d.chunks]
        lib.index(indexed)
    repo.save(lib)

    handler = FindSimilarChunksHandler(repo)

    req = FindSimilarRequest(
        embedding=list(lib.get_indexed_chunks()[0].embedding.values)
        if lib.get_indexed_chunks()
        else [0.0],
        k=2,
    )
    res = find_similar_chunks(library_id=str(lib.id), req=req, handler=handler)
    assert res.library_id == str(lib.id)
    assert isinstance(res.chunks, list)


def test_find_similar_chunks_presentation_with_filters(
    library_factory, document_factory
):
    repo = InMemoryLibraryRepository()
    lib = library_factory()
    # ensure there is an indexed chunk available for the search
    if not lib.get_indexed_chunks():
        d = document_factory()
        indexed = [IndexedChunk.from_chunk(c, d.id) for c in d.chunks]
        lib.index(indexed)
    repo.save(lib)

    handler = FindSimilarChunksHandler(repo)

    req = FindSimilarRequest(
        embedding=list(lib.get_indexed_chunks()[0].embedding.values)
        if lib.get_indexed_chunks()
        else [0.0],
        k=2,
        filters={"source": "test"},
    )
    res = find_similar_chunks(library_id=str(lib.id), req=req, handler=handler)
    assert res.library_id == str(lib.id)
    assert isinstance(res.chunks, list)
    # ensure returned chunks (if any) conform to the requested filter
    assert all(c.metadata.source == "test" for c in res.chunks)
