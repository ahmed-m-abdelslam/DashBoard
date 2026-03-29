from concurrent.futures import ThreadPoolExecutor, as_completed
from ai.client import groq_client, is_ai_available
from config import GROQ_MODEL, AI_TEMPERATURE, AI_TIMEOUT


def _call_groq(prompt):
    if not is_ai_available():
        return "AI analysis unavailable — API key not configured."
    try:
        completion = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=AI_TEMPERATURE,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"AI summary unavailable: {str(e)}"


def generate_project_summary(project):
    prompt = f"""You are a senior procurement analyst. Provide a concise executive summary (3-4 sentences) covering:
1. Current procurement status and progress assessment
2. Key risks or concerns identified
3. Recommended immediate actions
Be specific with numbers. Use professional tone.

Project: {project.get("project_name")} | Stage: {project.get("current_stage")}
Opening: {project.get("opening_date")} | Days Left: {project.get("days_to_opening", "N/A")}
Budget: {project.get("effective_budget")} {project.get("currency")}
Committed: {project.get("committed_spend")} | Utilization: {project.get("budget_utilization_pct", 0):.1f}%
Packages: {project.get("packages_completed")}/{project.get("total_packages")} completed
POs: {project.get("delivered_pos")}/{project.get("total_pos")} delivered
Overall Completion: {project.get("overall_completion")}%
Risk Score: {project.get("risk_score")}/100
Concerns: {'; '.join(project.get("concerns", [])) or 'None'}"""
    return _call_groq(prompt)


def generate_portfolio_summary(all_data):
    lines = []
    for d in all_data:
        lines.append(f"- {d['project_name']}: {d['overall_completion']:.0f}% complete, Risk: {d['risk_score']}/100, Opening: {d['opening_date']}")

    total_budget = sum(d["effective_budget"] for d in all_data)
    total_committed = sum(d["committed_spend"] for d in all_data)
    avg_completion = sum(d["overall_completion"] for d in all_data) / len(all_data)
    at_risk = sum(1 for d in all_data if d["risk_score"] >= 50)

    prompt = f"""You are a senior procurement portfolio manager. Analyze this portfolio:
1. Portfolio health assessment (1 sentence)
2. Top 2-3 critical issues across all projects
3. Strategic recommendations (2-3 bullet points)

Stats: {len(all_data)} projects, Avg completion: {avg_completion:.0f}%,
Total budget: {total_budget:,.0f}, Committed: {total_committed:,.0f}, At-risk: {at_risk}

Projects:
{chr(10).join(lines)}

Keep under 120 words. Be specific and actionable."""
    return _call_groq(prompt)


def generate_all_project_summaries(all_data, max_workers=4):
    if not is_ai_available():
        return {d["project_name"]: "AI unavailable." for d in all_data}

    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {executor.submit(generate_project_summary, d): d["project_name"] for d in all_data}
        for future in as_completed(future_map):
            name = future_map[future]
            try:
                results[name] = future.result(timeout=AI_TIMEOUT)
            except Exception:
                results[name] = "AI summary timed out."
    return results
