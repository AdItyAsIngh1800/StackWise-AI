from __future__ import annotations

from evidence.language_signals import get_language_signal


def build_features(context: dict, language: str) -> list[float]:
    signals = get_language_signal(language)
    team_languages = context.get("team_languages", [])

    return [
        1 if context.get("project_type") == "api" else 0,
        1 if context.get("expected_scale") == "high" else 0,
        1 if context.get("low_ops", False) else 0,
        1 if context.get("prefer_enterprise", False) else 0,
        1 if context.get("prototype_only", False) else 0,
        1 if context.get("rapid_schema_changes", False) else 0,
        1 if context.get("needs_cache", False) else 0,
        1 if context.get("prefer_portability", False) else 0,
        1 if language in team_languages else 0,
        float(signals.get("ecosystem", 0.0)),
        float(signals.get("activity", 0.0)),
        float(signals.get("popularity", 0.0)),
    ]