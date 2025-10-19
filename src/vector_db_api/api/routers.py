from fastapi import APIRouter

documents_router = APIRouter(prefix="/documents", tags=["documents"])
libraries_router = APIRouter(prefix="/libraries", tags=["libraries"])
