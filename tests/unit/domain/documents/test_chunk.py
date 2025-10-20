from datetime import timedelta

import pytest

from app.errors import InvalidEntityError


def test_chunk_requires_non_empty_text(chunk_factory):
    with pytest.raises(InvalidEntityError):
        chunk_factory(text="   ")


def test_matches_filter_source_and_page_number(chunk_factory):
    c = chunk_factory(text="ok", page=2)
    assert c.matches_filter({"source": "test"})
    assert not c.matches_filter({"source": "other"})
    assert c.matches_filter({"page_number": 2})
    assert not c.matches_filter({"page_number": 3})


def test_matches_filter_created_before_after(chunk_factory, now_utc):
    yesterday = now_utc - timedelta(days=1)
    two_days_ago = now_utc - timedelta(days=2)

    c_recent = chunk_factory(created_at=yesterday)

    # created_after should be True for timestamps earlier than created_at
    assert c_recent.matches_filter({"created_after": two_days_ago})
    # created_after should be False for timestamps after created_at
    assert not c_recent.matches_filter({"created_after": now_utc})

    # created_before should be True for timestamps later than created_at
    assert c_recent.matches_filter({"created_before": now_utc})
    # created_before should be False for timestamps earlier than created_at
    assert not c_recent.matches_filter({"created_before": two_days_ago})


def test_chunk_update_text_and_embedding_and_metadata(chunk_factory):
    c = chunk_factory(text="original", page=1)

    # update text
    c.update(text="updated")
    assert c.text == "updated"

    # update embedding
    c.update(embedding=[2.0, 3.0])
    assert c.embedding.values == (2.0, 3.0)

    # update metadata: source and custom fields
    c.update(metadata={"source": "newsrc", "custom_fields": {"k": "v"}})
    assert c.metadata.source == "newsrc"
    assert c.metadata.custom_fields.get("k") == "v"


def test_chunk_metadata_updated_at_changes_on_update(chunk_factory):
    c = chunk_factory(text="orig")
    before = c.metadata.updated_at
    c.update(metadata={"source": "s2"})
    assert c.metadata.updated_at > before


def test_chunk_update_invalid_text_raises(chunk_factory):
    c = chunk_factory(text="ok")

    with pytest.raises(InvalidEntityError):
        c.update(text="   ")


def test_matches_filter_multiple_conditions(chunk_factory):
    c = chunk_factory(text="ok", page=2)
    # both conditions true
    assert c.matches_filter({"source": "test", "page_number": 2})
    # one condition mismatched
    assert not c.matches_filter({"source": "test", "page_number": 3})


def test_matches_filter_unknown_key_is_ignored(chunk_factory):
    c = chunk_factory(text="ok")
    # unknown filter keys are ignored by the implementation and should not
    # cause a mismatch (legacy behavior preserved)
    assert c.matches_filter({"nonexistent": "value"})
