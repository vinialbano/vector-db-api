import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import pytest

from app.infrastructure import InMemoryDocumentRepository, InMemoryLibraryRepository
from app.domain.documents import Document, DocumentId, DocumentMetadata
from app.domain.libraries import Library, LibraryId, LibraryMetadata
from app.errors import NotFoundError


def _make_doc(i: int) -> Document:
    return Document(
        id=DocumentId.generate(), chunks=[], metadata=DocumentMetadata(title=f"d{i}")
    )


def _make_lib(i: int) -> Library:
    return Library(
        id=LibraryId.generate(),
        documents=[],
        metadata=LibraryMetadata(name=f"l{i}", description="test"),
        vector_index=None,
    )


def test_document_repository_concurrent_writes_reads():
    repo = InMemoryDocumentRepository()
    # create a pool of documents
    docs = [_make_doc(i) for i in range(200)]

    # worker that saves a document, possibly reads it back, sometimes deletes
    def worker_save_read_delete(doc: Document):
        try:
            repo.save(doc)
            # random read
            _ = repo.find_by_id(doc.id)
            # sometimes delete
            if random.random() < 0.1:
                try:
                    repo.delete(doc.id)
                except NotFoundError:
                    # delete may race; that's acceptable
                    pass
        except Exception:
            # re-raise to be caught by the test harness
            raise

    # run many concurrent operations
    with ThreadPoolExecutor(max_workers=16) as ex:
        futures = [
            ex.submit(worker_save_read_delete, d) for d in docs for _ in range(3)
        ]
        for fut in as_completed(futures):
            # any unexpected exception will surface here
            fut.result()

    # final consistency: all remaining items should be findable and no exceptions
    for d in docs:
        try:
            _ = repo.find_by_id(d.id)
        except Exception as exc:
            pytest.fail(f"Unexpected exception during final find_by_id: {exc}")


def test_library_repository_mixed_operations():
    repo = InMemoryLibraryRepository()
    libs = [_make_lib(i) for i in range(100)]

    lock = threading.Lock()
    ids = []

    def add_then_query(lib: Library):
        repo.save(lib)
        with lock:
            ids.append(lib.id)
        # random queries
        if random.random() < 0.5:
            _ = repo.find_all()
        if random.random() < 0.3:
            _ = repo.exists(lib.id)

    def delete_random():
        # delete a random id if available
        with lock:
            if not ids:
                return
            lid = ids.pop(random.randrange(len(ids)))
        try:
            repo.delete(lid)
        except NotFoundError:
            # acceptable in races
            pass

    tasks = []
    with ThreadPoolExecutor(max_workers=12) as ex:
        for lib in libs:
            tasks.append(ex.submit(add_then_query, lib))
        # add some deletes concurrently
        for _ in range(200):
            tasks.append(ex.submit(delete_random))

        for t in as_completed(tasks):
            t.result()

    # final pass: ensure find_all runs and no unexpected exceptions
    try:
        all_libs = repo.find_all()
        # smoke-check the result is a list
        assert isinstance(all_libs, list)
    except Exception as exc:
        pytest.fail(f"Unexpected exception during final find_all: {exc}")
