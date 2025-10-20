from app.errors import NotFoundError
from app.infrastructure import InMemoryDocumentRepository


def test_inmemory_document_repository_crud(document_factory):
    repo = InMemoryDocumentRepository()

    doc = document_factory()
    assert not repo.exists(doc.id)

    repo.save(doc)
    assert repo.exists(doc.id)

    found = repo.find_by_id(doc.id)
    assert found is doc

    all_docs = list(repo._store.values())
    assert doc in all_docs

    repo.delete(doc.id)
    assert not repo.exists(doc.id)

    # deleting again should raise NotFoundError

    try:
        repo.delete(doc.id)
        assert False, "expected NotFoundError"
    except NotFoundError:
        pass
