from typing import List

from app.parsers.base import BaseParser
from app.parsers.strategies.parsing_strategies import ParsingStrategy, PyMuPdfParser, DoclingParser, OCRParser


class PdfParser(BaseParser):
    def __init__(self, strategies:List[ParsingStrategy] = None):
        self.strategies = strategies or []

        
    def parse(self, doc_path):
        pages = [{"page_num": i, "page": page} for i, page in enumerate(doc_path)]
        result = []
        for page in page_dict:
            strategies: List[ParsingStrategy] = self.select_parsing_strategy(page)
            for strategy in strategies:
                result.append(strategy.parse_page(page))

    def select_parsing_strategy(self, page)->List[ParsingStrategy]:
        strategies = []

        # 1. Try PyMuPDF text extraction
        text = page.get_text().strip()
        if text:
            strategies.append(PyMuPdfParser())

            # 2. If text is there but you need semantic structure, add DocLing
            if len(text.split()) > 50:  # example heuristic: large text blocks
                strategies.append(DoclingParser())
        else:
            # 3. If no text found, fall back to OCR
            strategies.append(OCRParser())

        return strategies



