"""Script to load some data in s3."""
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.services import embedding, s3, wikipedia

wiki_api = wikipedia.WikipediaService()
s3_manager = s3.S3Service()
embedder = embedding.EmbeddingGenerator()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

articles_to_retrieve = [
    "FastAPI",
    "ASGI",
    "RESTful API",
    "OAuth",
    "JSON Schema",
    "Swagger (software)",
    "OpenAPI",
    "CORS",

    "Amazon Web Services",
    "AWS Lambda",
    "Amazon S3",
    "Amazon DynamoDB",
    "Amazon Elastic Compute Cloud",
    "Amazon SageMaker",
    "OpenSearch",

    # Inteligencia Artificial y Machine Learning
    "Machine Learning",
    "Deep Learning",
    "Natural Language Processing",
    "Transformer (deep learning architecture)",
    "Multimodal learning",
    "Generative pre-trained transformer",
    "OpenAI",
    "Llama (language model)",
    "Mistral AI",
    "Hugging Face",
    "Vector database",
    "Embedding"
]


def fetch_chunkize_and_upload() -> list:
    """Load articles."""
    for title in articles_to_retrieve:
        chunks = []
        try:
            document = wiki_api.fetch_article_by_name(title)
        except Exception:
            print(f"Article {title} not found.")
            continue
        chunks = [{
            "title": document["title"],
            "text": chunk,
            "embedding": embedder.generate_embedding(chunk)
        } for chunk in text_splitter.split_text(document["content"])]
        s3_manager.load_json(f"{document['title']}_embedding", chunks)


if __name__ == "__main__":
    fetch_chunkize_and_upload()
