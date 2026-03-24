from __future__ import annotations

from evidence.language_signals import get_language_signal


def build_features(context: dict, language: str) -> list[float]:
    signals = get_language_signal(language)

    return [
        1 if context["project_type"] == "api" else 0,
        1 if context["expected_scale"] == "high" else 0,
        1 if context["low_ops"] else 0,
        signals["ecosystem"],
        signals["activity"],
        signals["popularity"],
    ]