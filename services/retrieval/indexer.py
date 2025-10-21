from typing import Dict, List, Any

class DocumentIndex:
    def __init__(self):
        # {filename: {"chunks": List[str], "embeddings": np.ndarray}}
        self.store: Dict[str, Dict[str, Any]] = {}

    def add_document(self, filename: str, chunks: List[str]):
        self.store[filename] = {"chunks": chunks, "embeddings": None}

    def set_embeddings(self, filename: str, embeddings):
        if filename in self.store:
            self.store[filename]["embeddings"] = embeddings

    def get_document_chunks(self, filename: str) -> List[str]:
        return self.store.get(filename, {}).get("chunks", [])

    def get_embeddings(self, filename: str):
        return self.store.get(filename, {}).get("embeddings", None)

    def docs(self) -> List[str]:
        return list(self.store.keys())
