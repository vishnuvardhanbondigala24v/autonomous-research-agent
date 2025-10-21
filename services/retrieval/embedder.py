from sentence_transformers import SentenceTransformer
import numpy as np

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def encode(self, texts):
        if not texts:
            return None
        return self.model.encode(texts, normalize_embeddings=True)

    def encode_query(self, query: str):
        return self.encode([query])[0]

    def cosine_similarity_matrix_single(self, q_vec, emb_matrix):
        return np.dot(emb_matrix, q_vec)
