from app.dependencies.s3 import get_s3
from app.services.pdf_pipeline import PdfPipeline


class PipeLineFactory:
    @staticmethod
    def get_pipeline(doc_type: str):
        if doc_type.lower() == "pdf":
            return PdfPipeline(get_s3())
        return None