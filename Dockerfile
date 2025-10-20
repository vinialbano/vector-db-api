FROM python:3.14-slim

# Prevents Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies required to build some Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 755 /install.sh && /install.sh && rm /install.sh

# Set up the UV environment path
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Copy project metadata first to install dependencies (layer caching)
COPY pyproject.toml pyproject.toml

RUN uv sync

# Copy application source
COPY . .

# Expose the port the app runs on
EXPOSE $PORT

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
