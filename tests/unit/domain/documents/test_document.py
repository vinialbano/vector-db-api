def test_document_allows_empty_initial_chunks(document_factory):
    # documents may be created with an empty chunk list and filled later
    doc = document_factory(chunks=[])
    assert doc.chunk_count == 0


def test_document_add_remove_chunk(document_factory, chunk_factory):
    c1 = chunk_factory("one")
    c2 = chunk_factory("two")

    doc = document_factory(chunks=[c1])

    assert doc.chunk_count == 1

    doc.add_chunk(c2)
    assert doc.chunk_count == 2

    # remove one chunk (not last)
    doc.remove_chunk(c2.id)
    assert doc.chunk_count == 1

    # removing last chunk is allowed; document becomes empty
    doc.remove_chunk(c1.id)
    assert doc.chunk_count == 0


def test_document_update_chunk_delegates(document_factory, chunk_factory):
    c = chunk_factory(text="old", page=1)
    doc = document_factory(chunks=[c])

    # update via aggregate
    doc.update_chunk(c.id, text="new", embedding=[0.5, 0.5], metadata={"source": "x"})

    assert doc.chunks[0].text == "new"
    assert doc.chunks[0].metadata.source == "x"


def test_document_metadata_updated_at_changes(document_factory):
    doc = document_factory()
    before = doc.metadata.updated_at
    doc.update_metadata(title="New")
    assert doc.metadata.updated_at > before


def test_document_touch_metadata_on_add_remove_update(document_factory, chunk_factory):
    doc = document_factory()
    before = doc.metadata.updated_at

    # adding a chunk should touch metadata
    c = chunk_factory()
    doc.add_chunk(c)
    assert doc.metadata.updated_at > before

    # removing a chunk should touch metadata
    before2 = doc.metadata.updated_at
    doc.remove_chunk(c.id)
    assert doc.metadata.updated_at > before2

    # update chunk touches metadata
    c2 = chunk_factory()
    doc.add_chunk(c2)
    before3 = doc.metadata.updated_at
    doc.update_chunk(c2.id, text="changed")
    assert doc.metadata.updated_at > before3
