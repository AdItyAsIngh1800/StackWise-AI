from __future__ import annotations

import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

LANGUAGE_DESCRIPTIONS = {
    "python": "easy to use backend language with a rich ecosystem for APIs, data, and machine learning",
    "javascript": "web-focused language used for frontend and backend development with broad ecosystem support",
    "typescript": "typed javascript suited for scalable web applications and maintainable codebases",
    "java": "enterprise backend language for large systems, strong tooling, and mature frameworks",
    "go": "fast backend language for scalable systems, microservices, and efficient concurrency",
    "rust": "high performance language focused on safety, reliability, and systems programming",
}


def embed_text(text: str) -> np.ndarray:
    embedding = model.encode(text)
    return np.array(embedding, dtype=float)


def build_language_embeddings() -> dict[str, np.ndarray]:
    embeddings: dict[str, np.ndarray] = {}

    for language, description in LANGUAGE_DESCRIPTIONS.items():
        embeddings[language] = embed_text(description)

    return embeddings


LANGUAGE_EMBEDDINGS = build_language_embeddings()


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    if denominator == 0:
        return 0.0
    return float(np.dot(a, b) / denominator)


def semantic_search(query: str, top_k: int = 3) -> list[dict[str, float | str]]:
    query_vector = embed_text(query)

    results: list[dict[str, float | str]] = []
    for language, language_vector in LANGUAGE_EMBEDDINGS.items():
        similarity = cosine_similarity(query_vector, language_vector)
        results.append(
            {
                "language": language,
                "similarity": round(similarity, 4),
            }
        )

    results.sort(key=lambda item: float(item["similarity"]), reverse=True)
    return results[:top_k]