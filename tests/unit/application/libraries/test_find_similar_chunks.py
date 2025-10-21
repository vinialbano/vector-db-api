from app.application.libraries import FindSimilarChunksHandler, FindSimilarChunksQuery
from app.domain.libraries.indexed_chunk import IndexedChunk
from app.errors import InvalidEntityError
from app.infrastructure import InMemoryLibraryRepository


def test_find_similar_chunks_happy_path(library_factory, document_factory):
    repo = InMemoryLibraryRepository()
    lib = library_factory()
    # ensure the library has an index built (factory may or may not)
    # create a document with chunks and index them into the library
    doc = document_factory()
    indexed = [IndexedChunk.from_chunk(c, doc.id) for c in doc.chunks]
    lib.index(indexed)
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


def test_find_similar_chunks_with_filters(library_factory, document_factory):
    repo = InMemoryLibraryRepository()
    lib = library_factory()
    # create a document with chunks and index them into the library
    # create two chunks with different 'source' metadata so filters can be applied
    doc = document_factory(
        chunks=[
            document_factory().chunks[0],
        ]
    )
    # ensure we have two different sources by creating a second chunk manually
    from app.domain.common import Embedding
    from app.domain.documents import Chunk, ChunkId, ChunkMetadata

    c1 = doc.chunks[0]
    c2 = Chunk(
        id=ChunkId.generate(),
        text="other",
        embedding=Embedding.from_list(list(c1.embedding.values)),
        metadata=ChunkMetadata(source="other_source"),
    )
    indexed = [IndexedChunk.from_chunk(c, doc.id) for c in [c1, c2]]
    lib.index(indexed)
    repo.save(lib)

    handler = FindSimilarChunksHandler(repo)
    sample_embedding = list(lib.get_indexed_chunks()[0].embedding.values)
    # apply a filter that should only match the first chunk's source
    q = FindSimilarChunksQuery(
        library_id=str(lib.id),
        embedding=sample_embedding,
        k=5,
        filters={"source": "test"},
    )
    res = handler.handle(q)
    assert isinstance(res.chunks, list)
    # all returned chunks should have metadata.source == 'test'
    assert all(ch["metadata"]["source"] == "test" for ch in res.chunks)


def test_find_similar_chunks_library_not_found():
    repo = InMemoryLibraryRepository()
    handler = FindSimilarChunksHandler(repo)

    try:
        handler.handle(FindSimilarChunksQuery(library_id="nope", embedding=[0.0], k=1))
        assert False, "expected InvalidEntityError"
    except InvalidEntityError:
        pass
