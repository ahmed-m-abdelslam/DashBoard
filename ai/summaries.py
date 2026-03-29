from concurrent.futures import ThreadPoolExecutor, as_completed
from ai.client import groq_client, is_ai_available
from config import GROQ_MODEL, AI_TEMPERATURE
import os


AI_TIMEOUT = int(os.getenv("AI_TIMEOUT", "20"))


def _call_groq(prompt):
    if not is_ai_available():
        return "AI analysis unavailable — API key not configured."
    try:
        completion = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=AI_TEMPERATURE,
            max_tokens=300,  # ← حد أقصى عشان يرد أسرع
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"AI unavailable: {str(e)}"


def generate_project_summary(project):
    prompt = f"""Senior procurement analyst. Give 2-3 sentence executive summary:
Project: {project.get("project_name")} | Completion: {project.get("overall_completion")}%
Budget util: {project.get("budget_utilization_pct", 0):.0f}% | Risk: {project.get("risk_score")}/100
Packages: {project.get("packages_completed")}/{project.get("total_packages")}
POs: {project.get("delivered_pos")}/{project.get("total_pos")}
Opening: {project.get("opening_date")}
Concerns: {'; '.join(project.get("concerns", [])) or 'None'}
Be specific, concise, actionable."""
    return _call_groq(prompt)


def generate_portfolio_summary(all_data):
    lines = [
        f"- {d['project_name']}: {d['overall_completion']:.0f}%, Risk:{d['risk_score']}"
        for d in all_data
    ]
    total_budget = sum(d["effective_budget"] for d in all_data)
    avg = sum(d["overall_completion"] for d in all_data) / len(all_data)
    at_risk = sum(1 for d in all_data if d["risk_score"] >= 50)

    prompt = f"""Portfolio manager. Analyze in under 80 words:
{len(all_data)} projects, Avg completion: {avg:.0f}%, Budget: {total_budget:,.0f}, At-risk: {at_risk}
{chr(10).join(lines)}
Give: 1) Health assessment 2) Top issues 3) Actions"""
    return _call_groq(prompt)


def generate_all_project_summaries(all_data, max_workers=4):
    if not is_ai_available():
        return {d["project_name"]: "AI unavailable." for d in all_data}

    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(generate_project_summary, d): d["project_name"]
            for d in all_data
        }
        for future in as_completed(future_map):
            name = future_map[future]
            try:
                results[name] = future.result(timeout=AI_TIMEOUT)
            except Exception:
                results[name] = "AI summary timed out."
    return results
