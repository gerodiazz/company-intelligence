import pipeline
import intelligence
from db.repository import save_report
from graph.state import ResearchState


def gather_data(state: ResearchState) -> dict:
    try:
        result = pipeline.analyze_company(
            state["company"], state["url"], state.get("github_org")
        )
        return {"raw_events": result["events"]}
    except Exception as e:
        return {"error": str(e), "raw_events": []}


def analyze(state: ResearchState) -> dict:
    if state.get("error"):
        return {}
    try:
        insights = intelligence.generate_insights(
            state["company"], state["raw_events"]
        )
        return {"insights": insights}
    except Exception as e:
        return {"error": str(e)}


def save_to_db(state: ResearchState) -> dict:
    if state.get("error"):
        return {}
    try:
        save_report(state)
    except Exception as e:
        return {"error": str(e)}
    return {}


def generate_report(state: ResearchState) -> dict:
    if state.get("error"):
        return {"report": f"# Error\n\n{state['error']}"}
    try:
        c = state["company"]
        ins = state["insights"]

        techs = "\n".join(f"- {t}" for t in ins.get("technologies", []))
        signals = "\n".join(f"- {s}" for s in ins.get("signals", []))
        actionable = "\n".join(f"- {i}" for i in ins.get("insights", []))

        report = f"""# Reporte de Inteligencia: {c}

## Resumen
Análisis de tecnologías, señales de mercado e insights accionables para **{c}**.

## Tecnologías
{techs or "_Sin datos_"}

## Scores
| Métrica | Valor |
|---|---|
| Innovation Score | {ins.get("innovation_score", "N/A")} / 100 |
| Tech Maturity Score | {ins.get("tech_maturity_score", "N/A")} / 100 |

## Señales
{signals or "_Sin señales detectadas_"}

## Insights accionables
{actionable or "_Sin insights disponibles_"}
"""
        return {"report": report.strip()}
    except Exception as e:
        return {"error": str(e), "report": f"# Error generando reporte\n\n{e}"}
