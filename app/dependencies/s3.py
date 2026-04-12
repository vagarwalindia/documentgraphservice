from functools import lru_cache

from infrastructure.s3.s3_client import S3Client


@lru_cache(maxsize=1)
def get_s3():
    return S3Client()