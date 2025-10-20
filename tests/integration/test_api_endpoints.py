import pytest
from fastapi.testclient import TestClient

from app.container import (
    _document_repository_instance,
    _library_repository_instance,
)
from app.main import app

# no direct domain imports needed in these integration tests

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_repos():
    # Clear the in-memory repositories between tests
    _document_repository_instance.clear()
    _library_repository_instance.clear()
    yield


def test_health_check():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "healthy"}


def test_create_and_get_document():
    payload = {
        "metadata": {"title": "Doc 1", "author": "A"},
        "chunks": [{"text": "hello", "embedding": [1.0, 0.0], "metadata": {}}],
    }
    r = client.post("/documents/", json=payload)
    assert r.status_code == 201
    data = r.json()
    doc_id = data["document_id"]

    # fetch the document
    r2 = client.get(f"/documents/{doc_id}")
    assert r2.status_code == 200
    doc = r2.json()
    assert doc["document_id"] == doc_id
    assert doc["chunk_count"] == 1


def test_add_get_update_delete_chunk_flow():
    # create document
    payload = {"metadata": {"title": "Doc 2"}}
    r = client.post("/documents/", json=payload)
    doc_id = r.json()["document_id"]

    # add chunk
    chunk_payload = {"text": "c1", "embedding": [1.0, 0.0], "metadata": {}}
    r = client.post(f"/documents/{doc_id}/chunks", json=chunk_payload)
    assert r.status_code == 201
    chunk_id = r.json()["chunk_id"]

    # get chunk
    r = client.get(f"/documents/{doc_id}/chunks/{chunk_id}")
    assert r.status_code == 200

    # update chunk
    r = client.patch(f"/documents/{doc_id}/chunks/{chunk_id}", json={"text": "updated"})
    assert r.status_code == 204

    # delete chunk
    r = client.delete(f"/documents/{doc_id}/chunks/{chunk_id}")
    assert r.status_code == 204

    # get chunk should 404
    r = client.get(f"/documents/{doc_id}/chunks/{chunk_id}")
    assert r.status_code == 404


def test_library_flow_and_find_similar():
    # create a doc
    r = client.post(
        "/documents/",
        json={
            "metadata": {"title": "Doc 3"},
            "chunks": [{"text": "c", "embedding": [1.0, 0.0], "metadata": {}}],
        },
    )
    doc_id = r.json()["document_id"]

    # create library
    lib_payload = {"metadata": {"name": "L"}, "documents": [doc_id]}
    r = client.post("/libraries/", json=lib_payload)
    assert r.status_code == 201
    lib_id = r.json()["library_id"]

    # index library
    r = client.patch(f"/libraries/{lib_id}/index")
    assert r.status_code == 204

    # find similar (should return 200 and list)
    q = {"embedding": [1.0, 0.0], "k": 1}
    r = client.post(f"/libraries/{lib_id}/find-similar", json=q)
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, dict)
    assert "chunks" in body and isinstance(body["chunks"], list)


def test_invalid_id_returns_422():
    # malformed uuid should return 422 from InvalidEntityError mapping
    r = client.get("/documents/not-a-uuid")
    assert r.status_code == 422
