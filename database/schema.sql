-- Drop old tables (only for development reset)
DROP TABLE IF EXISTS recommendation_runs;
DROP TABLE IF EXISTS scenarios;

-- ---------------------------
-- Scenarios Table
-- ---------------------------
CREATE TABLE scenarios (
    id SERIAL PRIMARY KEY,
    scenario_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------
-- Recommendation Runs Table
-- ---------------------------
CREATE TABLE recommendation_runs (
    id SERIAL PRIMARY KEY,

    scenario_id INTEGER REFERENCES scenarios(id) ON DELETE SET NULL,

    project_type VARCHAR(100) NOT NULL,
    team_languages JSONB NOT NULL,
    input_payload JSONB NOT NULL,

    winner_language VARCHAR(100),
    winner_framework VARCHAR(100),
    winner_database VARCHAR(100),
    winner_deployment VARCHAR(100),
    winner_score DOUBLE PRECISION,

    confidence DOUBLE PRECISION,
    explanation TEXT,

    response_payload JSONB NOT NULL,
    sensitivity_payload JSONB,
    pareto_payload JSONB,
    why_not_payload JSONB,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------
-- Indexes (Performance)
-- ---------------------------
CREATE INDEX idx_runs_created_at ON recommendation_runs(created_at);
CREATE INDEX idx_runs_scenario_id ON recommendation_runs(scenario_id);
CREATE INDEX idx_runs_language ON recommendation_runs(winner_language);

CREATE INDEX idx_scenarios_name ON scenarios(scenario_name);