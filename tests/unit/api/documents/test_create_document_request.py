from app.api.documents.v1.create_document import (
    CreateDocumentRequest,
    create_document,
)
from app.application.documents import CreateDocumentHandler
from app.infrastructure import InMemoryDocumentRepository


def test_create_document_endpoint(document_factory):
    repo = InMemoryDocumentRepository()
    handler = CreateDocumentHandler(repo)

    req = CreateDocumentRequest(
        metadata={"title": "Doc title"},
        chunks=[
            {"text": "hello", "embedding": [1.0, 0.0], "metadata": {"source": "test"}}
        ],
    )
    res = create_document(req, handler=handler)

    assert res.document_id is not None
    from app.domain.documents import DocumentId

    assert repo.exists(DocumentId.from_string(res.document_id))
    # verify chunk persisted
    doc = repo.find_by_id(DocumentId.from_string(res.document_id))
    assert doc is not None
    assert doc.chunk_count == 1
    assert doc.chunks[0].text == "hello"
