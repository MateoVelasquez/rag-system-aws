"""Pipeline Module."""

from ..config import settings
from .embedding import EmbeddingGenerator
from .llm import LLM
from .retrieval import OpenSearchRetrieve


class RAGPipeline:
    """RAG Flow:.

    user_query -> embeddings -> retrieval open search -> LLM answer.
    """
    def __init__(self) -> None:
        """Pipeline init."""
        self.embedder = EmbeddingGenerator(settings.EMBEDDING_MODEL)
        self.retriever = OpenSearchRetrieve(
            settings.AWS_OPENSEARCH_HOST,
            settings.AWS_OPENSEARCH_USER,
            settings.AWS_OPENSEARCH_PASSWORD,
            port = settings.AWS_OPENSEARCH_PORT,
        )
        self.llm = LLM(settings.LLM_MODEL, settings.LLM_PROMPT)

    def generate_answer(self, question: str) -> str:
        """Generate answer."""
        embedding_question = self.embedder.generate_embedding(question)
        open_search_index = self.retriever.knn_search(
            settings.AWS_OPENSEARCH_INDEX_NAME, embedding_question
        )
        return self.llm.generate_response(question, open_search_index[0])
