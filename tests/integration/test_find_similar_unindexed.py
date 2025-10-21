from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_find_similar_unindexed_returns_409():
    # Create a library through the API (so it uses the same in-memory repo)
    create_res = client.post(
        "/libraries",
        json={
            "metadata": {
                "name": "IntegrationLib",
                "description": "test",
                "custom_fields": {},
            },
            "documents": [],
        },
    )
    assert create_res.status_code == 201
    lib = create_res.json()

    # call the API endpoint - we intentionally don't build the index
    res = client.post(
        f"/libraries/{lib['library_id']}/find-similar",
        json={"embedding": [0.0], "k": 1},
    )

    assert res.status_code == 409
    body = res.json()
    assert "error" in body and body["error"] == "Index not built"
    assert "details" in body
