from fastapi import FastAPI

from src.api.v1.endpoints import create_document, health, search_document

app = FastAPI(title="Embeddings API with DDD + OpenAI + LangChain")
app.include_router(health.router, prefix="/v1")
app.include_router(create_document.router, prefix="/v1")
app.include_router(search_document.router, prefix="/v1")
