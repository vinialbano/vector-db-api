from vector_db_api.api.documents.v1.get_chunk import get_chunk
from vector_db_api.application.documents import GetChunkHandler
from vector_db_api.infrastructure import InMemoryDocumentRepository


def test_get_chunk_presentation(document_factory):
    repo = InMemoryDocumentRepository()
    doc = document_factory()
    repo.save(doc)

    handler = GetChunkHandler(repo)
    chunk = doc.chunks[0]
    res = get_chunk(document_id=str(doc.id), chunk_id=str(chunk.id), handler=handler)
    assert res.chunk_id == str(chunk.id)
    assert res.text == chunk.text
