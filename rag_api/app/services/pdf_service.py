from pypdf import PdfReader

class PDFService:

    @staticmethod
    def extract_text(file_path: str) -> list[dict]:
        """returns a list of dicts like
        [
            {"page_number": 1, "text": "This is a sample text"},
            {"page_number": 2, "text": "This is another sample text"},
            {"page_number": 3, "text": "This is yet another sample text"},
        ]
        """

        reader = PdfReader(file_path)
        pages = []

        for idx, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            pages.append({"page_number": idx, "text": text.strip(),})

        return pages