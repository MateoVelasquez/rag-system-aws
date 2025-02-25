#! python3
"""This function is designed for use in AWS Lambda.

It retrieves a processed embedding file from S3 and loads it into an OpenSearch index.
"""
import base64
import json
import os
import urllib.parse
import urllib.request

import boto3

s3 = boto3.client("s3")

OPENSEARCH_ENDPOINT = os.getenv("AWS_OPENSEARCH_HOST")
INDEX_NAME = os.getenv("AWS_OPENSEARCH_INDEX_NAME", "rag-system-index")
AUTH = f"{os.getenv('AWS_OPENSEARCH_USER')}:{os.getenv('AWS_OPENSEARCH_PASSWORD')}"
auth_bytes = AUTH.encode("utf-8")
auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

HEADERS = {
    "Authorization": f"Basic {auth_base64}",
    "Content-Type": "application/json"
}

def lambda_handler(event, context) -> dict:  # noqa: ANN001, ARG001
    """Lambda function to index documents in OpenSearch triggered by s3."""
    # take s3 event.
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(record["s3"]["object"]["key"], encoding="utf-8")

    try:
        # Get file embedding from S3.
        response = s3.get_object(Bucket=bucket, Key=key)
        file_content = response["Body"].read().decode("utf-8")
        documents = json.loads(file_content)

        if not isinstance(documents, list):
            msg = "El archivo JSON no contiene una lista de documentos"
            raise TypeError(msg)  # noqa: TRY301

        # Process
        for document in documents:
            title = document.get("title", "")
            text = document.get("text", "")
            embedding = document.get("embedding", [])

            # Build document
            payload = json.dumps({
                "title": title,
                "text": text,
                "embedding": embedding
            }).encode("utf-8")

            url = f"{OPENSEARCH_ENDPOINT}/{INDEX_NAME}/_doc"
            if not url.startswith(("http:", "https:")):
                msg = "URL must start with 'http:' or 'https:'"
                raise ValueError(msg)  # noqa: TRY301

            # request HTTP with urllib
            req = urllib.request.Request(  # noqa: S310
                url,
                data=payload,
                headers=HEADERS,
                method="POST"
            )

            # Realiza la solicitud
            with urllib.request.urlopen(req) as res:  # noqa: S310
                result = json.loads(res.read().decode("utf-8"))

            print(
                f"Documento indexado correctamente: \
                    {key}, ID: {result.get('_id', 'N/A')}"
            )

        return {
            "statusCode": 200,
            "body": f"Se procesaron {len(documents)} documentos correctamente"
        }

    except Exception as e:
        print(f"Error al procesar {key}: {e}")
        return {"statusCode": 500, "body": str(e)}
