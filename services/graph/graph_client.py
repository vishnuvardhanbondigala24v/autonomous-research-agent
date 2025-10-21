from typing import List, Tuple
import re

def extract_triples(chunks: List[str]) -> List[Tuple[str, str, str]]:
    """
    Simple triple extractor:
    - Looks for 'X is Y', 'X consists of Y', 'X includes Y'
    Demo only; replace with NLP library for production.
    """
    triples = []
    patterns = [
        (r"([\w\s\-]+?)\s+is\s+(.*?)\.", "is"),
        (r"([\w\s\-]+?)\s+consists of\s+(.*?)\.", "consists_of"),
        (r"([\w\s\-]+?)\s+includes\s+(.*?)\.", "includes"),
    ]
    for ch in chunks:
        text = re.sub(r"\s+", " ", ch)
        for pat, rel in patterns:
            for m in re.finditer(pat, text, flags=re.IGNORECASE):
                subj = m.group(1).strip()
                obj = m.group(2).strip()
                if subj and obj:
                    triples.append((subj, rel, obj))
    return triples
