from __future__ import annotations

from typing import Any

from evidence.language_signals import get_language_signal

CANDIDATES = ["python", "javascript", "typescript", "java", "go", "rust"]


def _normalize_languages(value: Any) -> list[str]:
    if value is None:
        return []

    if isinstance(value, list):
        return [str(x).strip().lower() for x in value]

    return [str(value).strip().lower()]


def build_features(context: dict[str, Any], language: str) -> dict[str, float | int]:
    project_type = str(context.get("project_type", "")).strip().lower()
    expected_scale = str(context.get("expected_scale", "")).strip().lower()
    recommended_language = str(context.get("recommended_language", "")).strip().lower()
    team_languages = _normalize_languages(context.get("team_languages", []))
    language = language.strip().lower()

    signals = get_language_signal(language)

    return {
        "project_type_api": int(project_type == "api"),
        "project_type_web": int(project_type == "web"),

        "expected_scale_low": int(expected_scale == "low"),
        "expected_scale_medium": int(expected_scale == "medium"),
        "expected_scale_high": int(expected_scale == "high"),

        "low_ops": int(bool(context.get("low_ops"))),
        "prefer_enterprise": int(bool(context.get("prefer_enterprise"))),
        "prototype_only": int(bool(context.get("prototype_only"))),
        "rapid_schema_changes": int(bool(context.get("rapid_schema_changes"))),
        "needs_cache": int(bool(context.get("needs_cache"))),
        "prefer_portability": int(bool(context.get("prefer_portability"))),

        "candidate_python": int(language == "python"),
        "candidate_javascript": int(language == "javascript"),
        "candidate_typescript": int(language == "typescript"),
        "candidate_java": int(language == "java"),
        "candidate_go": int(language == "go"),
        "candidate_rust": int(language == "rust"),

        "team_knows_python": int("python" in team_languages),
        "team_knows_javascript": int("javascript" in team_languages),
        "team_knows_typescript": int("typescript" in team_languages),
        "team_knows_java": int("java" in team_languages),
        "team_knows_go": int("go" in team_languages),
        "team_knows_rust": int("rust" in team_languages),

        "team_has_candidate_language": int(language in team_languages),

        "ecosystem": float(signals.get("ecosystem", 0.0)),
        "activity": float(signals.get("activity", 0.0)),
        "popularity": float(signals.get("popularity", 0.0)),

        "is_recommended_language": int(language == recommended_language),
    }