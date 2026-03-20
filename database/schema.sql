CREATE TABLE IF NOT EXISTS recommendation_logs (
    id SERIAL PRIMARY KEY,
    project_type VARCHAR(100) NOT NULL,
    team_languages JSONB NOT NULL,
    low_ops BOOLEAN NOT NULL DEFAULT FALSE,
    expected_scale VARCHAR(50) NOT NULL,
    prefer_enterprise BOOLEAN NOT NULL DEFAULT FALSE,
    prototype_only BOOLEAN NOT NULL DEFAULT FALSE,
    rapid_schema_changes BOOLEAN NOT NULL DEFAULT FALSE,
    needs_cache BOOLEAN NOT NULL DEFAULT FALSE,
    prefer_portability BOOLEAN NOT NULL DEFAULT FALSE,

    winner_language VARCHAR(100),
    winner_framework VARCHAR(100),
    winner_database VARCHAR(100),
    winner_deployment VARCHAR(100),
    winner_score DOUBLE PRECISION,

    recommendation_payload JSONB NOT NULL,
    explanation TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);