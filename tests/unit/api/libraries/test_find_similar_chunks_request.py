from app.api.libraries.v1.find_similar_chunks import (
    FindSimilarRequest,
    find_similar_chunks,
)
from app.application.libraries import FindSimilarChunksHandler
from app.infrastructure import InMemoryLibraryRepository


def test_find_similar_chunks_presentation(library_factory):
    repo = InMemoryLibraryRepository()
    lib = library_factory()
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
