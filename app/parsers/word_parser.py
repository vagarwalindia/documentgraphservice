from app.parsers.base import BaseParser
from docx_parser import DocumentParser

class WordParser(BaseParser):
    def __init__(self, word_parser: DocumentParser):
        self.word_parser = word_parser

    def parse(self, doc_path):
        doc = DocumentParser(doc_path)
        doc.parse()

