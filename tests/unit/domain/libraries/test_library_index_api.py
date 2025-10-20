from app.domain.libraries.indexes.brute_force_index import BruteForceIndex
# no direct imports required



class BrokenIndex:
    def build(self, chunks):
        pass

    def search(self, query, k):
        return []

    def clear(self):
        pass

    def get_chunks(self):
        raise RuntimeError("broken index")


def test_get_indexed_chunks_propagates_error(library_factory):
    lib = library_factory()
    lib.vector_index = BrokenIndex()

    try:
        lib.get_indexed_chunks()
        assert False, "expected RuntimeError"
    except RuntimeError:
        pass
