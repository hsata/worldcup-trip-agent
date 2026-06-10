"""LLM-as-a-judge evaluator that grades agent responses."""

import json
import os
from google import genai

# Store evaluations in memory for the session
evaluation_history = []


async def evaluate_response(user_query: str, agent_response: str) -> dict:
    """Use Gemini to evaluate the agent's response quality."""
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    

    eval_prompt = f"""You are an expert evaluator for a World Cup 2026 travel assistant 
designed for first-time international travelers to North America.

Rate the following agent response on these criteria (1-5 each):

1. RELEVANCE: Does the response actually answer what the user asked?
2. SPECIFICITY: Does it give specific names, prices, neighborhoods — not vague advice?
3. CULTURAL_SENSITIVITY: Does it consider the traveler's background, dietary needs, cultural context?
4. ACCURACY: Is the information factually plausible and consistent?
5. ACTIONABILITY: Can the user actually act on this advice to plan their trip?

USER QUERY: {user_query}

AGENT RESPONSE: {agent_response[:3000]}

Respond ONLY with a JSON object, no other text:
{{"relevance": <1-5>, "specificity": <1-5>, "cultural_sensitivity": <1-5>, "accuracy": <1-5>, "actionability": <1-5>, "overall": <1-5>, "weakest_area": "<name of lowest scoring criterion>", "improvement_suggestion": "<one specific suggestion to improve>"}}"""

    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=eval_prompt,
        )
        result_text = response.text.strip()
        # Clean markdown fences if present
        result_text = result_text.replace("```json", "").replace("```", "").strip()
        scores = json.loads(result_text)

        evaluation = {
            "query": user_query,
            "scores": scores,
            "overall": scores.get("overall", 3),
            "weakest_area": scores.get("weakest_area", "unknown"),
            "suggestion": scores.get("improvement_suggestion", ""),
        }
        evaluation_history.append(evaluation)
        return evaluation

    except Exception as e:
        return {"error": str(e), "scores": {}, "overall": 0}


def get_evaluation_summary() -> dict:
    """Get a summary of all evaluations so far."""
    if not evaluation_history:
        return {"message": "No evaluations yet.", "count": 0}

    total = len(evaluation_history)
    avg_overall = sum(e["overall"] for e in evaluation_history) / total

    # Find weakest areas
    weak_areas = {}
    for e in evaluation_history:
        area = e.get("weakest_area", "unknown")
        weak_areas[area] = weak_areas.get(area, 0) + 1

    worst_area = max(weak_areas, key=weak_areas.get) if weak_areas else "none"

    low_scoring = [
        {"query": e["query"], "overall": e["overall"], "suggestion": e["suggestion"]}
        for e in evaluation_history
        if e["overall"] <= 3
    ]

    return {
        "total_evaluations": total,
        "average_overall_score": round(avg_overall, 2),
        "most_common_weakness": worst_area,
        "weakness_counts": weak_areas,
        "low_scoring_responses": low_scoring,
        "all_suggestions": [e["suggestion"] for e in evaluation_history if e.get("suggestion")],
    }
