from __future__ import annotations

# Normalize dataset language names → system language IDs

LANGUAGE_NORMALIZATION = {
    "python": "python",
    "javascript": "javascript",
    "typescript": "typescript",
    "java": "java",
    "go": "go",
    "golang": "go",
    "rust": "rust",
    "c#": "csharp",
    "csharp": "csharp",
}


def normalize_language(name: str) -> str | None:
    if not isinstance(name, str):
        return None

    key = name.strip().lower()
    return LANGUAGE_NORMALIZATION.get(key)