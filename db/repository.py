from db.client import supabase


def save_report(state: dict) -> None:
    insights = state.get("insights", {})

    row = {
        "company": state.get("company"),
        "url": state.get("url"),
        "github_org": state.get("github_org"),
        "technologies": insights.get("technologies", []),
        "innovation_score": insights.get("innovation_score"),
        "tech_maturity_score": insights.get("tech_maturity_score"),
        "signals": insights.get("signals", []),
        "insights": insights.get("insights", []),
        "report_md": state.get("report"),
    }

    supabase.table("reports").insert(row).execute()
