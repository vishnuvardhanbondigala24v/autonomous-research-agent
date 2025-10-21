from pdfminer.high_level import extract_text as pdfminer_extract_text

def extract_text(path: str) -> str:
    return pdfminer_extract_text(path)
