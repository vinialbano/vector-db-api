# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Vector DB API is a lightweight REST API built with FastAPI that provides vector similarity search capabilities. The project demonstrates clean architecture principles with in-memory storage, multiple vector index implementations (KD-tree and brute-force), and a well-structured domain model.

## Development Commands

### Environment Setup
```bash
# Create virtualenv and install dependencies
python -m venv .venv
source .venv/bin/activate
uv sync
```

### Running the Application
```bash
# Local development with auto-reload
uvicorn app.main:app --reload

# Using Docker Compose (with live-reload)
docker compose up --build

# Build and run Docker manually
docker build -t vector-db-api:local .
docker run --rm -p 8000:8000 vector-db-api:local
```

### Testing
```bash
# Run all tests
pytest

# Run tests quietly (less verbose)
pytest -q

# Run specific test file
pytest tests/unit/domain/test_document.py

# Run specific test function
pytest tests/unit/domain/test_document.py::test_create_document

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/
```

### Configuration
Environment variables are loaded from `.env` (use `.env.example` as template):
- `VECTOR_INDEX_TYPE`: Choose vector index implementation (`kd` for KD-tree [default], `brute` for brute-force)

## Architecture

This codebase follows **Clean Architecture** with **Domain-Driven Design (DDD)** principles and **CQRS-inspired** patterns.

### Layer Structure

```
app/
├── domain/           # Pure business logic (entities, value objects, aggregates)
├── application/      # Use case orchestration (commands & queries)
├── api/              # HTTP layer (FastAPI routers, request/response models)
├── infrastructure/   # Data persistence (in-memory repositories)
├── dependencies.py   # Dependency injection configuration
├── errors.py         # Domain error hierarchy
└── main.py           # FastAPI app setup & exception handlers
```

**Dependency Rule**: Outer layers depend on inner layers. Domain layer has no external dependencies.

### Domain Layer (`app/domain/`)

The domain layer contains pure business logic organized around two main aggregates:

**Documents Domain** (`app/domain/documents/`):
- `Document` - Aggregate root managing a collection of chunks
- `Chunk` - Entity representing text with embedding and metadata
- `DocumentId`, `ChunkId` - Value objects (UUID-based identifiers)
- `DocumentMetadata`, `ChunkMetadata` - Immutable value objects with factory methods
- `DocumentRepository` - Abstract repository interface

**Libraries Domain** (`app/domain/libraries/`):
- `Library` - Aggregate root managing indexed chunks for similarity search
- `LibraryId` - Value object identifier
- `LibraryMetadata` - Immutable value object
- `IndexedChunk` - Lightweight DTO for index operations
- `LibraryRepository` - Abstract repository interface
- `VectorIndex` - Abstract interface for indexing strategies
  - `KDTreeIndex` - O(log n) search, better for lower dimensions
  - `BruteForceIndex` - O(n) search, exact nearest neighbor

**Common Domain** (`app/domain/common/`):
- `Embedding` - Value object for immutable vectors with cosine similarity and euclidean distance methods
- `@refresh_timestamp_after` - Decorator for automatic timestamp updates on aggregate mutations

**Key Patterns**:
- **Aggregates**: Document and Library are aggregate roots with clear boundaries
- **Value Objects**: All IDs and metadata use frozen dataclasses for immutability
- **Strategy Pattern**: `VectorIndex` is abstract; implementations are pluggable
- **Factory Methods**: `.updated()` methods on value objects enable controlled immutability
- **Invariants**: Domain validation enforced in constructors (raises `InvalidEntityError`)

### Application Layer (`app/application/`)

The application layer orchestrates domain logic using the Command/Query pattern:

**Structure**:
```
application/
├── documents/
│   ├── create_document_command.py
│   ├── add_chunk_command.py
│   ├── get_document_query.py
│   └── ... (other commands/queries)
└── libraries/
    ├── create_library_command.py
    ├── index_library_command.py
    ├── find_similar_chunks_query.py
    └── ... (other commands/queries)
```

**Each command/query file contains**:
1. Input DTO (command/query parameters)
2. Output DTO (result representation)
3. Handler class with `handle()` method

**Commands** (files ending in `*_command.py`): Mutate state, validate input, construct domain entities, write to repositories
**Queries** (files ending in `*_query.py`): Read-only, fetch data from repositories or indexes, return DTOs

### API Layer (`app/api/`)

The API layer exposes FastAPI HTTP endpoints:

**Structure**:
```
api/
├── documents/
│   ├── create_document.py       # POST /documents/
│   ├── get_document.py          # GET /documents/{id}
│   └── add_chunk.py             # POST /documents/{doc_id}/chunks
├── libraries/
│   ├── create_library.py        # POST /libraries/
│   ├── index_library.py         # PATCH /libraries/{lib_id}/index
│   └── find_similar_chunks.py   # POST /libraries/{lib_id}/find-similar
└── routers.py                    # Router composition
```

**Each endpoint file contains**:
1. APIRouter instance
2. Pydantic request/response models with examples
3. DI provider function (creates handler via `Depends()`)
4. Endpoint handler function that maps HTTP → Command/Query → Response

### Infrastructure Layer (`app/infrastructure/`)

Repository implementations:
- `InMemoryDocumentRepository` - Thread-safe in-memory storage using `RLock`
- `InMemoryLibraryRepository` - Thread-safe in-memory storage using `RLock`

Note: Data is not persisted across restarts. Repositories use dictionaries with thread locks for concurrent access in uvicorn's multi-threaded mode.

### Dependency Injection (`app/dependencies.py`)

**Singleton Repositories**:
```python
_document_repository_instance = InMemoryDocumentRepository()
_library_repository_instance = InMemoryLibraryRepository()
```

**Vector Index Factory**:
Configurable via `VECTOR_INDEX_TYPE` environment variable:
- `kd` - Returns `KDTreeIndex` (default)
- `brute` - Returns `BruteForceIndex`

Handlers receive dependencies through FastAPI's `Depends()` mechanism.

### Error Handling (`app/errors.py`)

Domain errors map to HTTP status codes in `main.py`:
- `InvalidEntityError` → 422 Unprocessable Entity (domain validation failures)
- `NotFoundError` → 404 Not Found (entity not found in repository)
- `IndexNotBuiltError` → 409 Conflict (library index not built before search)

## Testing Strategy

Tests mirror the application structure:

```
tests/
├── unit/
│   ├── api/              # Test HTTP request/response handling
│   ├── application/      # Test command/query handlers
│   ├── domain/           # Test entities, aggregates, invariants
│   └── infrastructure/   # Test repository implementations
├── integration/          # End-to-end API tests
└── conftest.py          # Pytest fixtures & factories
```

**Key Fixtures** (in `conftest.py`):
- `embedding` - Standard test vector
- `chunk_factory` - Creates chunks with overridable attributes
- `document_factory` - Creates documents with optional chunks
- `library_factory` - Creates libraries with optional documents
- `now_utc` - Current UTC timestamp

**Testing Conventions**:
- Unit tests validate single components in isolation
- Integration tests use FastAPI's `TestClient` for end-to-end flows
- Factories provide flexible test data creation
- Domain tests focus on invariants and business rules
- Application tests mock repositories and verify orchestration

## Adding New Features

### Adding a New Command (Write Operation)
1. Create command file in `app/application/{domain}/` (e.g., `update_chunk_command.py`)
2. Define command DTO with input parameters
3. Define result DTO for output
4. Implement handler class with `handle()` method
5. Add API endpoint in `app/api/{domain}/` with Pydantic models
6. Register router in `app/api/routers.py`
7. Add unit tests in `tests/unit/application/`
8. Add integration tests in `tests/integration/`

### Adding a New Query (Read Operation)
Follow same steps as command, but name file `*_query.py` and ensure handler is read-only.

### Adding a New Vector Index Implementation
1. Create new class in `app/domain/libraries/indexes/`
2. Implement `VectorIndex` abstract interface (`build()`, `search()`, `clear()`, `get_chunks()`)
3. Update `_default_vector_index_factory()` in `app/dependencies.py` to support new type
4. Add unit tests in `tests/unit/domain/libraries/indexes/`
5. Add integration tests comparing behavior with other implementations

### Modifying Domain Entities
1. Update entity in `app/domain/{domain}/`
2. Ensure invariants are validated in constructors or methods
3. Use `@refresh_timestamp_after` decorator on mutation methods
4. Update corresponding tests in `tests/unit/domain/`
5. Verify application and API layers handle changes correctly

## Important Conventions

### Value Objects
- All value objects (IDs, metadata, embeddings) are frozen dataclasses
- Use factory methods for construction: `DocumentId.generate()`, `Embedding.from_list()`
- Use `.updated()` methods to create modified copies of metadata

### Aggregates
- Document and Library are aggregate roots with clear boundaries
- All mutations go through aggregate methods (e.g., `document.add_chunk()`)
- Use `@refresh_timestamp_after` to auto-update `updated_at` timestamps

### Repositories
- Always program against abstract interfaces (`DocumentRepository`, `LibraryRepository`)
- Raise `NotFoundError` when entities don't exist
- Current implementations are in-memory and thread-safe but not persistent

### Error Handling
- Raise domain errors (`InvalidEntityError`, `IndexNotBuiltError`) for business rule violations
- Let FastAPI exception handlers in `main.py` convert to appropriate HTTP responses
- Application layer catches domain errors when needed for orchestration

## API Documentation

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Tools and Utilities

**Payload Generator** (`tools/payload_generator.py`):
Generate test data from Cohere embeddings:
```bash
export COHERE_API_KEY="your-key"
python tools/payload_generator.py --texts-file texts.txt
# or
python tools/payload_generator.py --text "Text 1" --text "Text 2"
```

Outputs document and chunk JSON payloads for API testing.
