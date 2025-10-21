from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_find_similar_with_filters_positive_match():
    # create two documents with different chunk sources
    payload1 = {
        "metadata": {"title": "Doc A"},
        "chunks": [
            {"text": "a", "embedding": [1.0, 0.0], "metadata": {"source": "srcA"}}
        ],
    }
    payload2 = {
        "metadata": {"title": "Doc B"},
        "chunks": [
            {"text": "b", "embedding": [1.0, 0.0], "metadata": {"source": "srcB"}}
        ],
    }

    r1 = client.post("/documents/", json=payload1)
    assert r1.status_code == 201
    doc1 = r1.json()

    r2 = client.post("/documents/", json=payload2)
    assert r2.status_code == 201
    doc2 = r2.json()

    # create library containing both documents
    lib_payload = {
        "metadata": {"name": "FilterLib"},
        "documents": [doc1["document_id"], doc2["document_id"]],
    }
    r = client.post("/libraries/", json=lib_payload)
    assert r.status_code == 201
    lib = r.json()

    # index library
    r = client.patch(f"/libraries/{lib['library_id']}/index")
    assert r.status_code == 204

    # search with filter for srcA -> expect only srcA chunk
    q = {"embedding": [1.0, 0.0], "k": 5, "filters": {"source": "srcA"}}
    r = client.post(f"/libraries/{lib['library_id']}/find-similar", json=q)
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, dict)
    assert "chunks" in body
    assert len(body["chunks"]) == 1
    assert body["chunks"][0]["metadata"]["source"] == "srcA"
