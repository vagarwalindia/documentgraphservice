from typing import List

from app.parsers.base import BaseParser
from app.parsers.strategies.parsing_strategies import ParsingStrategy, PyMuPdfParser, DoclingParser, OCRParser


class PdfParser(BaseParser):
    def __init__(self, strategies:List[ParsingStrategy] = None):
        self.strategies = strategies or [OCRParser(), DoclingParser(), PyMuPdfParser()]

        
    def parse(self, doc_path):
        pages = [{"page_num": i, "page": page} for i, page in enumerate(doc_path)]
        parse_data = []
        for page_dicts in pages:
            page = page_dicts["page"]
            strategies: List[ParsingStrategy] = self.select_parsing_strategy(page)
            for strategy in strategies:
                parse_data.append(strategy.parse_page(page))
        return parse_data

    def select_parsing_strategy(self, page) -> List[ParsingStrategy]:
        strategies = []
        blocks = page.get_text("blocks")
        if not blocks:
            return [self.strategies[0]]  # OCRParser

        need_pymupdf = False
        need_ocr = False
        need_docling = False

        for block in blocks:
            block_type = block[6]
            text = block[4].strip() if block_type == 0 else ""

            if block_type == 0 and text:
                need_pymupdf = True
                if len(text.split()) > 50:
                    need_docling = True
            elif block_type == 1:
                need_ocr = True

            # Early stopping if all strategies are already needed
            if need_pymupdf and need_ocr and need_docling:
                break

        # Append in order
        if need_ocr:
            strategies.append(self.strategies[0])
        if need_docling:
            strategies.append(self.strategies[1])
        if need_pymupdf:
            strategies.append(self.strategies[2])

        return strategies



