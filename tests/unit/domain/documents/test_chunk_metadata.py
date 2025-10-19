from datetime import datetime, timedelta, timezone

from vector_db_api.domain.documents.chunk_metadata import ChunkMetadata


def test_chunkmetadata_updated_preserves_created_at():
    orig = ChunkMetadata(source="s", page_number=1)
    created_at = orig.created_at

    updated = orig.updated(source="new")
    assert updated.created_at == created_at


def test_chunkmetadata_updated_overrides_and_merges():
    orig = ChunkMetadata(source="s", page_number=1, custom_fields={"a": 1})
    updated = orig.updated(page_number=2, custom_fields={"b": 2})

    assert updated.source == "s"
    assert updated.page_number == 2
    # custom fields are merged
    assert updated.custom_fields == {"a": 1, "b": 2}


def test_chunkmetadata_updated_none_does_not_change():
    orig = ChunkMetadata(source="s", page_number=1, custom_fields={"a": 1})
    updated = orig.updated()
    assert updated.source == "s"
    assert updated.page_number == 1
    assert updated.custom_fields == {"a": 1}


def test_chunkmetadata_matches_filter_basic():

    now = datetime.now(timezone.utc)
    m = ChunkMetadata(source="src", page_number=2, created_at=now)

    assert m.matches_filter({"source": "src"})
    assert not m.matches_filter({"source": "other"})
    assert m.matches_filter({"page_number": 2})
    assert not m.matches_filter({"page_number": 3})


def test_chunkmetadata_matches_filter_created_before_after():

    now = datetime.now(timezone.utc)
    earlier = now - timedelta(days=1)
    later = now + timedelta(days=1)

    m = ChunkMetadata(source="s", page_number=1, created_at=now)

    assert m.matches_filter({"created_after": earlier})
    assert not m.matches_filter({"created_after": later})

    assert m.matches_filter({"created_before": later})
    assert not m.matches_filter({"created_before": earlier})


def test_chunkmetadata_matches_filter_unknown_key_is_ignored():
    m = ChunkMetadata(source="s", page_number=1)
    # unknown keys should be ignored and not cause a mismatch
    assert m.matches_filter({"foo": "bar"})
