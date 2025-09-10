from typing import Optional

from openai import OpenAI

from src.domain.embeddings import EmbeddingGenerator


class OpenAIEmbeddingGenerator(EmbeddingGenerator):
    def __init__(self, api_key: Optional[str] = None, model: str = "text-embedding-3-large"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def embed(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(model=self.model, input=texts)
        return [d.embedding for d in response.data]
