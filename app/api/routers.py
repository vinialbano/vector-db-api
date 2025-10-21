from fastapi import APIRouter

from app.api.documents.add_chunk import add_chunk_router
from app.api.documents.create_document import create_document_router
from app.api.documents.delete_chunk import delete_chunk_router
from app.api.documents.delete_document import delete_document_router
from app.api.documents.get_chunk import get_chunk_router
from app.api.documents.get_document import get_document_router
from app.api.documents.update_chunk import update_chunk_router
from app.api.documents.update_document import update_document_router
from app.api.libraries.add_document import add_document_router
from app.api.libraries.create_library import create_library_router
from app.api.libraries.delete_library import delete_library_router
from app.api.libraries.find_similar_chunks import find_similar_chunks_router
from app.api.libraries.get_library import get_library_router
from app.api.libraries.index_library import index_library_router
from app.api.libraries.remove_document import remove_document_router
from app.api.libraries.update_library import update_library_router

# Documents Router

documents_router = APIRouter(prefix="/documents")

documents_router.include_router(add_chunk_router, tags=["chunks"])
documents_router.include_router(get_chunk_router, tags=["chunks"])
documents_router.include_router(delete_chunk_router, tags=["chunks"])
documents_router.include_router(update_chunk_router, tags=["chunks"])

documents_router.include_router(create_document_router, tags=["documents"])
documents_router.include_router(get_document_router, tags=["documents"])
documents_router.include_router(delete_document_router, tags=["documents"])
documents_router.include_router(update_document_router, tags=["documents"])

# Libraries Router

libraries_router = APIRouter(prefix="/libraries")

libraries_router.include_router(find_similar_chunks_router, tags=["chunks"])

libraries_router.include_router(add_document_router, tags=["documents"])
libraries_router.include_router(remove_document_router, tags=["documents"])

libraries_router.include_router(create_library_router, tags=["libraries"])
libraries_router.include_router(get_library_router, tags=["libraries"])
libraries_router.include_router(index_library_router, tags=["libraries"])
libraries_router.include_router(delete_library_router, tags=["libraries"])
libraries_router.include_router(update_library_router, tags=["libraries"])
