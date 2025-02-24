"""OpenSearch retriever module."""
import base64

from opensearchpy import OpenSearch, RequestsHttpConnection


class OpenSearchRetrieve:
    """Index Retriever."""

    def __init__(
        self,
        host: str,
        os_user: str,
        os_password: str,
        port: int = 443,
    ) -> None:
        """Index retriever init."""
        self.host = host
        self.port = port
        auth_str = f"{os_user}:{os_password}"
        auth_bytes = auth_str.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/json",
        }
        self.client = OpenSearch(
            hosts=[{"host": host, "port": port}],
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
            headers=headers,
        )

    def knn_search(
        self, index_name: str, query_embedding: list, top_k: int = 3
    ) -> list:
        """Search in OpenSearch with knn method."""
        response = self.client.search(
            index=index_name,
            body={
                "size": top_k,
                "query": {
                    "knn": {
                        "embedding": {
                            "vector": query_embedding,
                            "k": top_k,
                        }
                    }
                },
            },
        )
        return [hit["_source"]["text"] for hit in response["hits"]["hits"]]
