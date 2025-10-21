# Vector DB API

Lightweight Vector Database REST API built with FastAPI. This project provides a small domain model (Chunk, Document, Library), in-memory repositories, two vector index implementations (brute-force and KD-tree), application/service layers, and HTTP endpoints to CRUD documents/libraries and perform k-NN similarity search.

This repository was created as a take-home task to demonstrate clear design, testing, and basic operational support (Docker).

## Architectural approach

This project follows several complementary architectural patterns to keep the code organized and maintainable:

- Domain-Driven Design (DDD): core domain concepts (value objects, entities, aggregates, domain services) live under `app/domain`. Business invariants and domain logic belong here.
- Clean Architecture: layers are separated (API, Application, Domain, Infrastructure). The application layer orchestrates use-cases and keeps HTTP/controllers thin.
- Vertical Slice Architecture (VSA): features are co-located (for example `documents` routes, handlers, and related application/domain code are organized so a feature is easy to reason about and evolve), while still respecting layer boundaries.

This combination makes it straightforward to add or change features with minimal cross-cutting changes.

## Highlights

- FastAPI app with modular routers under `app/api`.
- Domain layer under `app/domain` (value objects, entities, aggregates, indexes).
- Application layer under `app/application` (commands/queries, handlers).
- In-memory repositories in `app/infrastructure` (thread-safe with RLock).
- Custom errors in `app/errors.py` mapped to HTTP statuses (InvalidEntityError -> 422, NotFoundError -> 404, IndexNotBuiltError -> 409).
- Unit tests and integration tests included (`tests/`).
- Dockerfile and `docker-compose.yml` for local development.

## Quickstart

Requirements: Python 3.13, Docker (optional)

Run locally (recommended in a virtualenv):

```bash
python -m venv .venv
source .venv/bin/activate
uv sync
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs for interactive API docs.

Run tests:

```bash
pytest -q
```

Docker (local dev with live-reload):

```bash
docker compose up --build
```

Or build/run the image manually:

```bash
docker build -t vector-db-api:local .
docker run --rm -p 8000:8000 vector-db-api:local
```

## Generating test payloads from Cohere

If you want to generate API-shaped document and chunk payloads from Cohere embeddings (for testing or seeding), there's a small helper in `tools/` that calls Cohere and writes JSON payloads.

Prerequisites:

- Export your Cohere API key: `export COHERE_API_KEY="sk-..."`.

Quick usage:

```bash
# generate payloads from a newline-delimited texts file
python tools/payload_generator.py --texts-file path/to/texts.txt

# or pass texts directly
python tools/payload_generator.py --text "First text" --text "Second text"
```

Outputs:

- `<out-dir>/run_<id>/<doc-name>` — a document payload (POST /documents shape).
- `<out-dir>/run_<id>/chunk_<i>.json` — one file per chunk (POST /documents/{id}/chunks shape).

## API Endpoints (examples)

- GET /health — health check
- POST /documents/ — create document
- GET /documents/{id} — fetch document
- POST /documents/{id}/chunks — add a chunk
- POST /libraries - create a library
- POST /libraries/{lib_id}/documents/{doc_id} - add document
- PATCH /libraries/{id}/index — build library index
- POST /libraries/{id}/find-similar — query k-NN

See full schemas and examples in the OpenAPI docs at `/docs` after starting the server.

## Design notes

- Index implementations

  - Brute-force index: O(n) query time, O(n) memory. Simple, exact nearest neighbor by scanning all vectors.
  - KD-tree index: faster for lower-dimensional data and read-heavy workloads; average query time O(log n) for balanced trees but degrades with high-dimensions.

  ## Choosing a vector index implementation

  You can choose which VectorIndex implementation the server will use when creating libraries. The selection is controlled by the environment variable `VECTOR_INDEX_TYPE`:

  - `kd` (default) — use the KDTreeIndex implementation
  - `brute` — use the BruteForceIndex implementation

  Examples

  Using the provided `docker-compose.yml` (the `web` service includes an `environment` entry):

  ```bash
  # Edit docker-compose.yml or override when running compose
  export VECTOR_INDEX_TYPE=brute
  docker compose up --build
  ```

  Or run locally with the variable set in your shell:

  ```bash
  export VECTOR_INDEX_TYPE=brute
  uvicorn app.main:app --reload
  ```

- Thread-safety

  - In-memory repositories use `threading.RLock` to protect the internal dict store. This prevents simple race conditions during concurrent accesses in a multi-threaded server (uvicorn default workers).
  - For heavy concurrent usage or multi-process deployment, use an external persistence (SQLite, Postgres) or move to a process-safe store.

- Error handling
  - Domain vs application errors are separated. `InvalidEntityError` signals client input or domain validation issues (mapped to HTTP 422). `NotFoundError` maps to HTTP 404.

## Next steps / improvements

- Persistence: add JSON/SQLite persistence to survive restarts.
- Metadata filtering: expose API support for meta-filtered k-NN queries.
- CI: add GitHub Actions to run tests on push/PR.
- Generate embeddings on demand, with Cohere API
- Optional: SDK client, temporal durable workflows, and leader-follower replication.
