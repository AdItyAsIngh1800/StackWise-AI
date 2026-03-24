#!/usr/bin/env bash
set -e

BASE_URL="http://127.0.0.1:8000"

echo "== Health =="
curl -s "$BASE_URL/health" | python -m json.tool

echo
echo "== Root =="
curl -s "$BASE_URL/" | python -m json.tool

echo
echo "== Recommend =="
curl -s -X POST "$BASE_URL/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "project_type": "api",
    "team_languages": ["python"],
    "low_ops": true,
    "expected_scale": "medium",
    "prefer_enterprise": false,
    "prototype_only": false,
    "rapid_schema_changes": false,
    "needs_cache": false,
    "prefer_portability": false
  }' | python -m json.tool

echo
echo "== Natural Language Recommend =="
curl -s -X POST "$BASE_URL/recommend/natural-language" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Build a scalable backend API with low ops using python"
  }' | python -m json.tool

echo
echo "== Semantic Search =="
curl -s "$BASE_URL/semantic-search?query=fast backend scalable&top_k=3" 

echo
echo "== Feedback =="
curl -s -X POST "$BASE_URL/feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "run_id": null,
    "project_type": "api",
    "expected_scale": "medium",
    "low_ops": true,
    "prefer_enterprise": false,
    "prototype_only": false,
    "rapid_schema_changes": false,
    "needs_cache": false,
    "prefer_portability": false,
    "team_languages": ["python"],
    "recommended_language": "python",
    "selected_language": "python"
  }' | python -m json.tool

echo
echo "== Analytics: Top Languages =="
curl -s "$BASE_URL/analytics/top-languages" | python -m json.tool

echo
echo "== Analytics: Confidence =="
curl -s "$BASE_URL/analytics/confidence" | python -m json.tool

echo
echo "== Analytics: Confidence Trend =="
curl -s "$BASE_URL/analytics/confidence-trend" | python -m json.tool

echo
echo "== Analytics: Project Types =="
curl -s "$BASE_URL/analytics/project-types" | python -m json.tool

echo
echo "== Analytics: Recent Runs =="
curl -s "$BASE_URL/analytics/recent-runs" | python -m json.tool

echo
echo "== ML Evaluation =="
curl -s "$BASE_URL/ml/evaluation" | python -m json.tool

echo
echo "✅ Backend smoke test complete."