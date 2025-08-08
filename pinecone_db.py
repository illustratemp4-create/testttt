from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_chunks(json_chunks: str) -> tuple[list[dict], np.ndarray]:
    chunks = json.loads(json_chunks)
    texts = [chunk['text'] for chunk in chunks]
    embeddings = model.encode(texts, normalize_embeddings=True)
    return chunks, embeddings


def search(query: str, chunks: list[dict], embeddings: np.ndarray, top_k: int = 5) -> list[str]:
    query_embedding = model.encode([query])
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = np.argpartition(-similarities, top_k)[:top_k]
    top_indices = top_indices[np.argsort(-similarities[top_indices])]
    return [chunks[i]['text'] for i in top_indices]
