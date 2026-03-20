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
    "c sharp": "csharp",
}


def normalize_language(name: str) -> str | None:
    if not isinstance(name, str):
        return None

    key = name.strip().lower()
    return LANGUAGE_NORMALIZATION.get(key)


LANGUAGE_TO_BACKEND_FRAMEWORKS = {
    "python": ["fastapi", "django"],
    "javascript": ["express"],
    "typescript": ["nestjs"],
    "java": ["spring-boot"],
    "go": ["gin"],
    "rust": [],
    "csharp": [],
}


LANGUAGE_TO_DATABASES = {
    "python": ["postgresql", "mongodb", "redis", "sqlite"],
    "javascript": ["postgresql", "mongodb", "redis"],
    "typescript": ["postgresql", "mongodb", "redis"],
    "java": ["postgresql", "mysql", "redis"],
    "go": ["postgresql", "redis"],
    "rust": ["postgresql", "sqlite"],
    "csharp": ["postgresql"],
}


LANGUAGE_TO_DEPLOYMENT = {
    "python": ["render", "railway", "docker-vm", "ecs"],
    "javascript": ["vercel", "render", "railway"],
    "typescript": ["vercel", "render", "railway", "docker-vm"],
    "java": ["docker-vm", "ecs", "kubernetes"],
    "go": ["docker-vm", "ecs", "kubernetes"],
    "rust": ["docker-vm", "fly-io"],
    "csharp": ["docker-vm", "azure-app-service"],
}