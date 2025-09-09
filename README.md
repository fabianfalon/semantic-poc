# Semantic POC

## Description

**Semantic POC** is a microservice built with **FastAPI** that ingests long documents (title + content), splits them into chunks with **LangChain**, converts those chunks into embeddings, and stores them in **PostgreSQL** with the **pgvector** extension. It exposes a clean REST API to create documents and run semantic search over the stored chunks.

The service follows a clean, modular, DDD-inspired architecture, making it easy to extend and maintain. It is designed to be consumed by other applications via HTTP in a decoupled and scalable way.

## Features

- 📄 Document ingestion (title + long text) and chunking via LangChain
- 🧠 Embeddings with OpenAI (text-embedding-3-large) or deterministic mocks (no external keys needed)
- 🗄️ Vector storage using PostgreSQL + pgvector (`Vector(3072)`) with similarity search `<->`
- 🧱 Clean, modular, DDD-inspired architecture (domain/application/infrastructure/api)
- 🧪 Ready for unit and integration testing
- 🚀 Automatic API docs with Swagger and ReDoc via FastAPI

## Requirements

- **Python 3.12+**
- **FastAPI**, **Uvicorn**
- **PostgreSQL** with **pgvector** (provided via Docker)
- Additional dependencies in `requirements.txt` and `requirements-tests.txt`

## Project Structure

```
semantic-poc/
├── infra/
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   └── docker-compose.yml
├── src/
│   ├── api/                     # API routers, dependencies, schemas
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── create_document.py
│   │       │   ├── search_document.py
│   │       │   └── health.py
│   │       ├── dependencies.py
│   │       └── schemas.py
│   ├── application/             # Application services (use cases)
│   │   ├── create_document.py
│   │   └── search_document.py
│   ├── domain/                  # Domain entities, interfaces, services
│   │   ├── content_text_spliter.py
│   │   ├── document.py
│   │   ├── document_repository.py
│   │   └── services.py
│   ├── infrastructure/          # Adapters (DB, text splitter, ORM)
│   │   ├── database.py
│   │   ├── text_splitter.py
│   │   └── postgresql/
│   │       └── repositories.py
│   ├── config.py
│   └── main.py                  # FastAPI entrypoint
├── tests/
├── requirements.txt
├── requirements-tests.txt
├── Dockerfile
├── Makefile
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd semantic-poc
```

### 2. Install dependencies (optional if you run via Docker)

```bash
pip install -r requirements.txt
```

### 3. Run the stack with Docker (recommended)

```bash
make up
```
This starts:
- `app`: FastAPI service on `http://localhost:8000`
- `db`: PostgreSQL with pgvector extension
- `adminer`: DB client at `http://localhost:8080`

Apply migrations (first time):
```bash
make alembic-rev m="init"
make alembic-up
```

Stop services:
```bash
make down
```

### 4. Environment variables

Create a `.env` at repo root (optional):
```
# Use OpenAI embeddings when provided
OPENAI_API_KEY=sk-...

# Force mock embeddings (deterministic 3072-dim vectors)
USE_EMBEDDINGS_MOCK=true
```
- When running outside Docker, set the database URL manually:
```
export DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/embeddings_db
```

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc UI**: http://localhost:8000/redoc

## Example Requests

### Create Document

```bash
curl -X POST "http://localhost:8000/v1/documents/" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "My title",
           "text": "Long content ..."
         }'
```

Response
```json
{
  "document": {
    "id": 1,
    "title": "My title",
    "content": "Long content ...",
    "created_at": "...",
    "updated_at": "..."
  },
  "chunks": [
    { "id": 1, "content": "chunk 1 ..." },
    { "id": 2, "content": "chunk 2 ..." }
  ]
}
```

### Search

```bash
curl "http://localhost:8000/v1/search/?query=python&limit=5"
```

Response
```json
[
  {
    "chunk_id": 10,
    "document_title": "My title",
    "content": "...",
    "similarity": "92.35 %"
  }
]
```

## Development Notes

- Splitting: `RecursiveCharacterTextSplitter` (tunable `CHUNK_SIZE`, `OVERLAP`)
- Embeddings:
  - If `OPENAI_API_KEY` is present and `USE_EMBEDDINGS_MOCK` is not set to true, the service uses OpenAI `text-embedding-3-large` (3072 dims)
  - Otherwise, it uses a deterministic mock (also 3072 dims) so create/search remain consistent without external services
- Storage:
  - SQLAlchemy ORM with a `Vector(3072)` column on `document_chunks`
  - Distance operator `<->` for similarity; the application turns distance into a percentage-like score

## Running Tests

```bash
pip install -r requirements-tests.txt
PYTHONPATH=. pytest
```
(or use `make test` if provided in the Makefile.)

## Roadmap

- [ ] Add pagination and metadata to search responses
- [ ] Plug-in support for alternative embedding providers
- [ ] Background ingestion pipeline and batch processing

---

### Quick Access

- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc
- **Adminer**: http://localhost:8080 (Server: `db`, User: `user`, Password: `password`, DB: `embeddings_db`) 