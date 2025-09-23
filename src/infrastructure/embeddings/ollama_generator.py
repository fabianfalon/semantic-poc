from langchain_ollama.embeddings import OllamaEmbeddings

from src.domain.embeddings import EmbeddingGenerator


class OllamaEmbeddingGenerator(EmbeddingGenerator):
    def __init__(self, model: str = "nomic-embed-text", base_url: str = "http://ollama:11434"):
        self.model = model
        self.base_url = base_url
        self.client = OllamaEmbeddings(model=self.model, base_url=self.base_url)

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self.client.embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        return self.client.embed_query(text)
