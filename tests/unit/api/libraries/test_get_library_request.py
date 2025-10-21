from app.api.libraries.get_library import get_library
from app.application.libraries import GetLibraryHandler
from app.infrastructure import InMemoryLibraryRepository


def test_get_library_presentation(library_factory):
    repo = InMemoryLibraryRepository()
    lib = library_factory()
    repo.save(lib)

    handler = GetLibraryHandler(repo)
    res = get_library(library_id=str(lib.id), handler=handler)
    assert res.library_id == str(lib.id)
    assert res.document_ids == [str(d) for d in lib.documents]
    assert res.metadata.name == lib.metadata.name
    assert isinstance(res.indexed_chunks, list)
