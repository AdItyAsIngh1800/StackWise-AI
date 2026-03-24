from __future__ import annotations

from typing import Any

LANGUAGE_KEYWORDS = {
    "python": "python",
    "javascript": "javascript",
    "typescript": "typescript",
    "java": "java",
    "go": "go",
    "rust": "rust",
    "c++": "c++",
    "c#": "c#",
    "php": "php",
}

PROJECT_TYPE_KEYWORDS = {
    "api": "api",
    "backend": "api",
    "web": "web",
    "frontend": "web",
    "ai": "ai-ml",
    "ml": "ai-ml",
    "machine learning": "ai-ml",
    "enterprise": "enterprise",
}

HIGH_SCALE_KEYWORDS = {
    "scalable",
    "high scale",
    "large scale",
    "enterprise scale",
    "millions",
    "heavy traffic",
}

LOW_OPS_KEYWORDS = {
    "low ops",
    "managed",
    "minimal ops",
    "easy deployment",
    "low maintenance",
}

CACHE_KEYWORDS = {
    "cache",
    "caching",
    "real-time",
    "realtime",
    "fast response",
    "low latency",
}

PROTOTYPE_KEYWORDS = {
    "prototype",
    "mvp",
    "quick build",
    "hackathon",
    "demo",
}

ENTERPRISE_KEYWORDS = {
    "enterprise",
    "large organization",
    "compliance",
    "strict process",
}

PORTABILITY_KEYWORDS = {
    "portable",
    "portability",
    "vendor neutral",
    "avoid lock-in",
}


def parse_natural_language_query(text: str) -> dict[str, Any]:
    q = text.strip().lower()

    project_type = "api"
    for key, value in PROJECT_TYPE_KEYWORDS.items():
        if key in q:
            project_type = value
            break

    expected_scale = "medium"
    if any(keyword in q for keyword in HIGH_SCALE_KEYWORDS):
        expected_scale = "high"
    elif "small" in q or "side project" in q or "personal project" in q:
        expected_scale = "small"

    low_ops = any(keyword in q for keyword in LOW_OPS_KEYWORDS)
    prefer_enterprise = any(keyword in q for keyword in ENTERPRISE_KEYWORDS)
    prototype_only = any(keyword in q for keyword in PROTOTYPE_KEYWORDS)
    needs_cache = any(keyword in q for keyword in CACHE_KEYWORDS)
    prefer_portability = any(keyword in q for keyword in PORTABILITY_KEYWORDS)
    rapid_schema_changes = (
        "schema change" in q
        or "changing schema" in q
        or "flexible schema" in q
    )

    team_languages: list[str] = []
    for keyword, language in LANGUAGE_KEYWORDS.items():
        if keyword in q and language not in team_languages:
            team_languages.append(language)

    return {
        "project_type": project_type,
        "team_languages": team_languages,
        "low_ops": low_ops,
        "expected_scale": expected_scale,
        "prefer_enterprise": prefer_enterprise,
        "prototype_only": prototype_only,
        "rapid_schema_changes": rapid_schema_changes,
        "needs_cache": needs_cache,
        "prefer_portability": prefer_portability,
    }