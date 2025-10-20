from app.domain.common import Embedding
from app.domain.documents import ChunkId, DocumentId
from app.domain.libraries.indexed_chunk import IndexedChunk


def make_indexed_chunk():
    cid = ChunkId.generate()
    did = DocumentId.generate()
    emb = Embedding.from_list([1.0, 0.0])
    return IndexedChunk(id=cid, document_id=did, text="hello", embedding=emb)


def test_similarity_and_dimension():
    ic = make_indexed_chunk()
    q = Embedding.from_list([1.0, 0.0])
    assert ic.similarity(q) == 1.0
    assert ic.dimension == 2


def test_distance():
    ic = make_indexed_chunk()
    q = Embedding.from_list([0.0, 0.0])
    assert ic.distance(q) > 0


def test_to_dict_contains_expected_keys():
    ic = make_indexed_chunk()
    d = ic.to_dict()
    assert "chunk_id" in d and "document_id" in d and "text" in d and "embedding" in d
