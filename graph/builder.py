from langgraph.graph import StateGraph, START, END

from graph.state import ResearchState
from graph.nodes import gather_data, analyze, generate_report, save_to_db


def _build() -> object:
    builder = StateGraph(ResearchState)

    builder.add_node("gather_data", gather_data)
    builder.add_node("analyze", analyze)
    builder.add_node("generate_report", generate_report)
    builder.add_node("save_to_db", save_to_db)

    builder.add_edge(START, "gather_data")
    builder.add_edge("gather_data", "analyze")
    builder.add_edge("analyze", "generate_report")
    builder.add_edge("generate_report", "save_to_db")
    builder.add_edge("save_to_db", END)

    return builder.compile()


research_graph = _build()
