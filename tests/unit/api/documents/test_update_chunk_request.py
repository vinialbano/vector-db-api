from app.api.documents.update_chunk import (
    UpdateChunkRequest,
    update_chunk,
)
from app.application.documents import UpdateChunkHandler
from app.infrastructure import InMemoryDocumentRepository


def test_update_chunk_endpoint(document_factory):
    repo = InMemoryDocumentRepository()
    handler = UpdateChunkHandler(repo)

    doc = document_factory()
    repo.save(doc)
    chunk = doc.chunks[0]

    req = UpdateChunkRequest(text="updated text")
    res = update_chunk(
        document_id=str(doc.id), chunk_id=str(chunk.id), request=req, handler=handler
    )

    assert res is None

    updated = repo.find_by_id(doc.id)
    assert updated.chunks[0].text == "updated text"
