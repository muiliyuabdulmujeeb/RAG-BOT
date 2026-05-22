from sentence_transformers import SentenceTransformer

from app.core.config import settings


class EmbeddingModelService:
    def __init__(self):
        self.model = SentenceTransformer(settings.embedding_model)
        self.model.max_seq_length = 256


    def embed(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True
        )
        return embeddings.tolist()