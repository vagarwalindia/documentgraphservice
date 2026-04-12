from abc import abstractmethod, ABC


class ParsingStrategy(ABC):
    @abstractmethod
    def parse_page(self,page):
        pass

class PyMuPdfParser(ParsingStrategy):
    def parse_page(self, page):
        return page.get_text()



class DoclingParser(ParsingStrategy):
    def parse_page(self, page):
        pass


class OCRParser(ParsingStrategy):
    def parse_page(self, page):
        pass