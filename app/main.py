from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from app.api.documents import documents_router
from app.api.libraries import libraries_router
from app.errors import InvalidEntityError, NotFoundError
from app.errors import IndexNotBuiltError

app = FastAPI(
    title="Vector DB API",
    description="An API for managing vector databases, libraries, and documents.",
    version="1.0.0",
)

app.include_router(documents_router)
app.include_router(libraries_router)


@app.get("/", include_in_schema=False)
def root():
    return {"message": "Welcome to the Vector DB API!", "docs": "/docs"}


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy"}


@app.exception_handler(InvalidEntityError)
def invalid_entity_handler(request, exc: InvalidEntityError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"error": "Invalid entity", "details": str(exc)},
    )


@app.exception_handler(NotFoundError)
def not_found_handler(request, exc: NotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "Not Found", "details": str(exc)},
    )


@app.exception_handler(IndexNotBuiltError)
def index_not_built_handler(request, exc: IndexNotBuiltError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"error": "Index not built", "details": str(exc)},
    )


@app.exception_handler(Exception)
def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal Server Error", "details": str(exc)},
    )
