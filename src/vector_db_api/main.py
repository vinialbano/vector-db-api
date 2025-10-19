from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from vector_db_api.api.documents import *  # noqa: F401, F403
from vector_db_api.api.libraries import *  # noqa: F401, F403
from vector_db_api.api.documents import *  # noqa: F401, F403
from vector_db_api.api.libraries import *  # noqa: F401, F403
from vector_db_api.api.routers import documents_router, libraries_router

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


@app.exception_handler(Exception)
def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal Server Error", "details": str(exc)},
    )
