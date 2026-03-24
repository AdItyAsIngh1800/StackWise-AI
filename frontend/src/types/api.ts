export type StackRecommendation = {
  language: string;
  score: number;
  backend_framework: string | null;
  database: string | null;
  deployment: string | null;
};

export type SensitivityVariation = {
  scenario: string;
  winner: string;
};

export type SimilarStack = {
  language: string;
  score: number;
  distance: number;
};

export type RecommendationResponse = {
  winner: StackRecommendation | null;
  alternatives: StackRecommendation[];
  ranked_languages: { language: string; score: number }[];
  explanation?: string | null;
  confidence?: number | null;
  sensitivity?: {
    base_winner?: string;
    stability?: number;
    variations?: SensitivityVariation[];
  } | null;
  pareto?: { language: string; score: number; ecosystem: number }[] | null;
  why_not?: { language: string; reason: string }[] | null;
  similar_stacks?: SimilarStack[] | null;
};

export type NaturalLanguageRecommendationResponse = {
  parsed_input: {
    project_type: string;
    team_languages: string[];
    low_ops: boolean;
    expected_scale: string;
    prefer_enterprise: boolean;
    prototype_only: boolean;
    rapid_schema_changes: boolean;
    needs_cache: boolean;
    prefer_portability: boolean;
  };
  recommendation: RecommendationResponse;
};

export type TopLanguage = {
  language?: string;
  winner_language?: string;
  count: number;
};

export type RecentRun = {
  id: number;
  project_type: string;
  winner_language: string;
  score: number;
  created_at: string;
};

export type ConfidenceTrendPoint = {
  date: string;
  avg_confidence: number | null;
};

export type ProjectTypeDistribution = {
  project_type: string;
  count: number;
};