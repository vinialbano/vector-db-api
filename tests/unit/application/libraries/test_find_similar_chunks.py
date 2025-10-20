from app.application.libraries import FindSimilarChunksHandler, FindSimilarChunksQuery
from app.errors import InvalidEntityError
from app.infrastructure import InMemoryLibraryRepository


def test_find_similar_chunks_happy_path(library_factory):
    repo = InMemoryLibraryRepository()
    lib = library_factory()
    # ensure the library has an index built (factory may or may not)
    repo.save(lib)

    handler = FindSimilarChunksHandler(repo)
    # use an embedding matching dimension from factory chunks (factory provides valid embedding)
    sample_embedding = (
        list(lib.get_indexed_chunks()[0].embedding.values)
        if lib.get_indexed_chunks()
        else [0.0]
    )
    q = FindSimilarChunksQuery(library_id=str(lib.id), embedding=sample_embedding, k=3)
    res = handler.handle(q)
    assert res.library_id == str(lib.id)
    assert isinstance(res.chunks, list)
    assert all(
        "similarity" in chunk and isinstance(chunk["similarity"], float)
        for chunk in res.chunks
    )


def test_find_similar_chunks_library_not_found():
    repo = InMemoryLibraryRepository()
    handler = FindSimilarChunksHandler(repo)

    try:
        handler.handle(FindSimilarChunksQuery(library_id="nope", embedding=[0.0], k=1))
        assert False, "expected InvalidEntityError"
    except InvalidEntityError:
        pass
