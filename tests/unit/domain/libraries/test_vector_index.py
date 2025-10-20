import pytest

from app.domain.common import Embedding
from app.domain.documents import ChunkId, ChunkMetadata, DocumentId
from app.domain.libraries import BruteForceIndex, KDTreeIndex
from app.domain.libraries.indexed_chunk import IndexedChunk
from app.errors import IndexNotBuiltError


@pytest.fixture
def sample_chunks():
    """Create sample chunks for testing"""
    return [
        IndexedChunk(
            id=ChunkId.generate(),
            document_id=DocumentId.generate(),
            text=f"Chunk {i}",
            embedding=Embedding.from_list([float(i), float(i * 2), float(i * 3)]),
            metadata=ChunkMetadata(source=f"source{i}"),
        )
        for i in range(10)
    ]


def test_search(sample_chunks):
    bf_index = BruteForceIndex()
    bf_index.build(sample_chunks)
    kd_index = KDTreeIndex()
    kd_index.build(sample_chunks)

    query = Embedding.from_list([1.0, 2.0, 3.0])
    bf_results = bf_index.search(query, k=3)
    kd_results = kd_index.search(query, k=3)

    assert len(bf_results) == 3
    assert len(kd_results) == 3
    assert all(isinstance(chunk, IndexedChunk) for chunk in bf_results)
    assert all(isinstance(chunk, IndexedChunk) for chunk in kd_results)


def test_index_with_filters(sample_chunks):
    bf_index = BruteForceIndex()
    bf_index.build(sample_chunks)
    kd_index = KDTreeIndex()
    kd_index.build(sample_chunks)

    query = Embedding.from_list([1.0, 2.0, 3.0])
    filters = {"source": "source1"}
    bf_results = bf_index.search(query, k=5, filters=filters)
    kd_results = kd_index.search(query, k=5, filters=filters)

    assert len(bf_results) == 1
    assert bf_results[0].metadata.source == "source1"
    assert len(kd_results) == 1
    assert kd_results[0].metadata.source == "source1"


def test_search_without_building_raises():
    bf_index = BruteForceIndex()
    kd_index = KDTreeIndex()

    query = Embedding.from_list([1.0, 2.0, 3.0])

    with pytest.raises(IndexNotBuiltError):
        bf_index.search(query, k=3)
    with pytest.raises(IndexNotBuiltError):
        kd_index.search(query, k=3)


def test_search_with_invalid_k_raises(sample_chunks):
    bf_index = BruteForceIndex()
    kd_index = KDTreeIndex()
    bf_index.build(sample_chunks)
    kd_index.build(sample_chunks)

    query = Embedding.from_list([1.0, 2.0, 3.0])
    from app.errors import InvalidEntityError

    with pytest.raises(InvalidEntityError):
        bf_index.search(query, k=0)
    with pytest.raises(InvalidEntityError):
        kd_index.search(query, k=-1)


def test_clear_index(sample_chunks):
    bf_index = BruteForceIndex()
    kd_index = KDTreeIndex()
    bf_index.build(sample_chunks)
    kd_index.build(sample_chunks)

    bf_index.clear()
    kd_index.clear()

    assert bf_index._chunks == []
    assert kd_index._root is None
    assert kd_index._dimension == 0
