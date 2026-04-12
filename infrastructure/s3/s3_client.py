import logging
from functools import lru_cache

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError
from infrastructure.config.settings import settings
from typing import Optional
import time


logger = logging.getLogger("s3_client")
logger.setLevel(logging.INFO)  # or DEBUG in dev





class S3Client:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key,
            aws_secret_access_key=settings.aws_secret_key,
            region_name=settings.aws_region,
        )
        self.max_retries = 3
        self.retry_backoff_sec = 2

    def fetch_document(self, bucket: str, key: str) -> Optional[bytes]:
        """Fetch document bytes from S3 with retries and logging."""
        attempt = 0
        while attempt < self.max_retries:
            try:
                logger.info(f"Fetching s3://{bucket}/{key}, attempt {attempt+1}")
                response = self.client.get_object(Bucket=bucket, Key=key)
                data = response["Body"].read()
                logger.info(f"Successfully fetched s3://{bucket}/{key}, size={len(data)} bytes")
                return data
            except EndpointConnectionError as e:
                logger.warning(f"Network issue fetching s3://{bucket}/{key}: {e}, retrying...")
            except ClientError as e:
                error_code = e.response['Error']['Code']
                logger.error(f"AWS ClientError fetching s3://{bucket}/{key}: {error_code} - {e}")
                # For 4xx errors, usually no point retrying
                if error_code.startswith("4"):
                    break
            except Exception as e:
                logger.error(f"Unexpected error fetching s3://{bucket}/{key}: {e}")

            attempt += 1
            time.sleep(self.retry_backoff_sec * attempt)

        logger.error(f"Failed to fetch s3://{bucket}/{key} after {self.max_retries} attempts")
        return None
