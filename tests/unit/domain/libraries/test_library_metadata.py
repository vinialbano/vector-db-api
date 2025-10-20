import pytest

from app.domain.libraries import LibraryMetadata
from app.errors import InvalidEntityError


def test_librarymetadata_updated_preserves_created_at():
    orig = LibraryMetadata(name="L", description="D")
    created_at = orig.created_at

    updated = orig.updated(name="New")
    assert updated.created_at == created_at


def test_librarymetadata_updated_overrides_and_merges():
    orig = LibraryMetadata(name="L", description="D", custom_fields={"x": 1})
    updated = orig.updated(description="NewD", custom_fields={"y": 2})

    assert updated.name == "L"
    assert updated.description == "NewD"
    # custom fields are merged shallowly
    assert updated.custom_fields == {"x": 1, "y": 2}


def test_librarymetadata_updated_none_does_not_change():
    orig = LibraryMetadata(name="L", description="D", custom_fields={"x": 1})
    updated = orig.updated()
    assert updated.name == "L"
    assert updated.description == "D"
    assert updated.custom_fields == {"x": 1}


def test_librarymetadata_requires_name():
    with pytest.raises(InvalidEntityError):
        LibraryMetadata(name="", description="desc")
