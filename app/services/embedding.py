"""Embedding generator module."""
from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    """Clase para manejar la generación de embeddings."""

    def __init__(
            self,
            model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
        ) -> None:
        """Init embeddings."""
        self.model_name = model_name
        self.embedding_model = SentenceTransformer(self.model_name)

    def generate_embedding(self, text: str) -> list:
        """Generate the embedding of a text."""
        return self.embedding_model.encode(text).tolist()
