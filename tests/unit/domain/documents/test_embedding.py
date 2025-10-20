import pytest

from app.domain.common.embedding import Embedding
from app.errors import InvalidEntityError


def test_embedding_creation():
    emb = Embedding.from_list([1.0, 2.0, 3.0])
    assert emb.dimension == 3


def test_embedding_immutable():
    emb = Embedding.from_list([1.0, 2.0, 3.0])
    with pytest.raises(AttributeError):
        emb.values = (4.0, 5.0, 6.0)


def test_cosine_similarity():
    emb1 = Embedding.from_list([1.0, 0.0, 0.0])
    emb2 = Embedding.from_list([1.0, 0.0, 0.0])
    assert emb1.cosine_similarity(emb2) == pytest.approx(1.0)

    emb3 = Embedding.from_list([0.0, 1.0, 0.0])
    assert emb1.cosine_similarity(emb3) == pytest.approx(0.0)


def test_embedding_different_dimensions_error():
    emb1 = Embedding.from_list([1.0, 2.0])
    emb2 = Embedding.from_list([1.0, 2.0, 3.0])

    with pytest.raises(InvalidEntityError):
        emb1.cosine_similarity(emb2)
