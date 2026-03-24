from __future__ import annotations

from typing import Any

import numpy as np

_MODEL: Any | None = None
_LANGUAGE_EMBEDDINGS: dict[str, np.ndarray] | None = None

LANGUAGE_DESCRIPTIONS = {
    "python": "easy to use backend language with a rich ecosystem for APIs, data, and machine learning",
    "javascript": "web-focused language used for frontend and backend development with broad ecosystem support",
    "typescript": "typed javascript suited for scalable web applications and maintainable codebases",
    "java": "enterprise backend language for large systems, strong tooling, and mature frameworks",
    "go": "fast backend language for scalable systems, microservices, and efficient concurrency",
    "rust": "high performance language focused on safety, reliability, and systems programming",
}


def get_model() -> Any:
    global _MODEL
    if _MODEL is None:
        from sentence_transformers import SentenceTransformer
        _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return _MODEL


def embed_text(text: str) -> np.ndarray:
    model = get_model()
    embedding = model.encode(text)
    return np.array(embedding, dtype=float)


def build_language_embeddings() -> dict[str, np.ndarray]:
    embeddings: dict[str, np.ndarray] = {}
    for language, description in LANGUAGE_DESCRIPTIONS.items():
        embeddings[language] = embed_text(description)
    return embeddings


def get_language_embeddings() -> dict[str, np.ndarray]:
    global _LANGUAGE_EMBEDDINGS
    if _LANGUAGE_EMBEDDINGS is None:
        _LANGUAGE_EMBEDDINGS = build_language_embeddings()
    return _LANGUAGE_EMBEDDINGS


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    if denominator == 0:
        return 0.0
    return float(np.dot(a, b) / denominator)


def semantic_search(query: str, top_k: int = 3) -> list[dict[str, float | str]]:
    query_vector = embed_text(query)
    language_embeddings = get_language_embeddings()

    results: list[dict[str, float | str]] = []
    for language, language_vector in language_embeddings.items():
        similarity = cosine_similarity(query_vector, language_vector)
        results.append(
            {
                "language": language,
                "similarity": round(similarity, 4),
            }
        )

    results.sort(key=lambda item: float(item["similarity"]), reverse=True)
    return results[:top_k]