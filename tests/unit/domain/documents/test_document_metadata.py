from vector_db_api.domain.documents import DocumentMetadata


def test_documentmetadata_updated_preserves_created_at():
    orig = DocumentMetadata(title="T", author="A")
    created_at = orig.created_at

    updated = orig.updated(title="New")
    assert updated.created_at == created_at


def test_documentmetadata_updated_overrides_and_merges():
    orig = DocumentMetadata(title="T", author="A", custom_fields={"x": 1})
    updated = orig.updated(author="B", custom_fields={"y": 2})

    assert updated.title == "T"
    assert updated.author == "B"
    # custom fields are merged shallowly
    assert updated.custom_fields == {"x": 1, "y": 2}


def test_documentmetadata_updated_none_does_not_change():
    orig = DocumentMetadata(title="T", author="A", custom_fields={"x": 1})
    updated = orig.updated()
    assert updated.title == "T"
    assert updated.author == "A"
    assert updated.custom_fields == {"x": 1}
