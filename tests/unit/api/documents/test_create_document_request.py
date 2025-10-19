from vector_db_api.api.documents.v1.create_document import (
    CreateDocumentRequest,
    create_document,
)
from vector_db_api.application.documents import CreateDocumentHandler
from vector_db_api.infrastructure import InMemoryDocumentRepository


def test_create_document_endpoint(document_factory):
    repo = InMemoryDocumentRepository()
    handler = CreateDocumentHandler(repo)

    req = CreateDocumentRequest(title="Doc title")
    res = create_document(req, handler=handler)

    assert res.document_id is not None
    from vector_db_api.domain.documents import DocumentId

    assert repo.exists(DocumentId.from_string(res.document_id))
