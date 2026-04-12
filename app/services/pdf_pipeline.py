from app.parsers.pdf_parser import PdfParser
from app.services.base_pipeline import AbstractPipeline


class PdfPipeline(AbstractPipeline):
    def __init__(self, s3_client):
        super().__init__(s3_client)
        self.parser = PdfParser()

    def parsing(self, doc_path):
        self.parser.parse(doc_path=doc_path)

    def cleaning(self, parse_data):
        pass

    def chunking(self, clean_data):
        pass

    def embedding(self, chunk_data):
        pass

    def store_to_db(self, embedded_data):
        pass