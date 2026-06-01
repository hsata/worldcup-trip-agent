"""Tool that lets the agent introspect on its own performance."""

from worldcup_agent.evaluator import get_evaluation_summary


def check_my_performance() -> dict:
    """Check how well I've been performing in this session. Returns evaluation scores,
    weakest areas, and suggestions for improvement.

    Returns:
        dict with performance summary including average scores, common weaknesses, and improvement suggestions
    """
    summary = get_evaluation_summary()

    if summary.get("count", -1) == 0:
        return {"message": "No evaluations recorded yet. Keep answering questions and I'll track my performance."}

    # Build adaptive guidance based on weaknesses
    guidance = []
    weakness = summary.get("most_common_weakness", "")

    if "specificity" in weakness.lower():
        guidance.append("I need to give more specific recommendations — exact restaurant names, prices, neighborhoods, not vague suggestions.")
    if "cultural" in weakness.lower():
        guidance.append("I should better consider the traveler's cultural background, dietary needs, and comfort level in unfamiliar environments.")
    if "actionability" in weakness.lower():
        guidance.append("My responses need more concrete next steps — booking links, specific timelines, exact costs.")
    if "relevance" in weakness.lower():
        guidance.append("I should focus more on directly answering what was asked before expanding into related topics.")
    if "accuracy" in weakness.lower():
        guidance.append("I should be more careful with facts — double-checking venue names, transit routes, and visa requirements.")

    summary["adaptive_guidance"] = guidance
    return summary
