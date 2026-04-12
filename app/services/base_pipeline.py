from typing import final
from abc import ABC, abstractmethod

from infrastructure.config.settings import settings


class AbstractPipeline(ABC):
    def __init__(self, s3_client):
        self.s3_client = s3_client
    @abstractmethod
    def parsing(self, doc_path):
        pass

    @abstractmethod
    def cleaning(self, parse_data):
        pass
    @abstractmethod
    def chunking(self, clean_data):
        pass
    @abstractmethod
    def embedding(self, chunk_data):
        pass
    @abstractmethod
    def store_to_db(self, embedded_data):
        pass
    def fetch_doc(self, key):
        return self.s3_client.fetch_document(bucket=settings.S3_BUCKET, key=key)


    """Don't override this method"""
    @final
    def process_document(self, event, doc_type):
        doc = self.fetch_doc(key=event["storageKey"])
        parse_data = self.parsing(doc=doc, doc_type=doc_type)
        clean_data = self.cleaning(parse_data=parse_data)
        chunk_data = self.chunking(clean_data=clean_data)
        embedded_data = self.embedding(chunk_data=chunk_data)
        self.store_to_db(embedded_data=embedded_data)

