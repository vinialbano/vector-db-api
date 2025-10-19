from vector_db_api.infrastructure.repositories import InMemoryDocumentRepository


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

    deleted = repo.delete(doc.id)
    assert deleted
    assert not repo.exists(doc.id)

    # deleting again returns False
    assert not repo.delete(doc.id)
