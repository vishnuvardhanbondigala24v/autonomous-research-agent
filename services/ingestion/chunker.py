from typing import List

def chunk_text(text: str, max_chars: int = 1200, overlap: int = 150) -> List[str]:
    """
    Chunk text by packing paragraphs into windows with overlap.
    - max_chars: maximum characters per chunk
    - overlap: number of trailing characters to carry into the next chunk
    """
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks: List[str] = []
    current = ""

    for p in paragraphs:
        if len(current) + len(p) + 1 <= max_chars:
            current = (current + " " + p).strip()
        else:
            if current:
                chunks.append(current)
            tail = current[-overlap:] if current else ""
            current = (tail + " " + p).strip()

    if current:
        chunks.append(current)

    return chunks if chunks else [text[:max_chars]]
