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
};