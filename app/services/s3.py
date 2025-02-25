"""S3 Service module."""
from io import BytesIO
import json
import logging

import boto3

from ..config import settings


class S3Service:
    """S3 Service."""
    def __init__(self) -> None:
        """Define client."""
        self.client = boto3.client('s3')

    def load_json(
            self,
            file_name: str,
            data: list,
            bucket_name: str = settings.S3_BUCKET_NAME
        ) -> None:
        """Load json to s3 bucket."""
        bucket_name = "rag-system-s3-bucket"
        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        json_bytes = BytesIO(json_data.encode("utf-8"))

        # Subir a S3 directamente desde memoria
        self.client.upload_fileobj(json_bytes, bucket_name, f"{file_name}.json")
        logging.info(
            "file loaded to S3: s3://%s/%s.json", bucket_name, file_name
        )
