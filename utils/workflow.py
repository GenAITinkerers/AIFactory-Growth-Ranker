from langgraph.graph import StateGraph, END
from state import AgentState
from agents.margin_agent import margin_analysis_agent
from agents.moat_agent import moat_analysis_agent
from agents.growth_agent import ranking_agent
from agents.report_agent import report_agent

def create_workflow():
    """Creates and compiles the LangGraph workflow."""
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("analyze_margin", margin_analysis_agent)
    workflow.add_node("analyze_moat", moat_analysis_agent)
    workflow.add_node("calculate_rank", ranking_agent)
    workflow.add_node("generate_report", report_agent)

    # Define the flow (Edges)
    workflow.set_entry_point("analyze_margin")
    workflow.add_edge("analyze_margin", "analyze_moat")
    workflow.add_edge("analyze_moat", "calculate_rank")
    workflow.add_edge("calculate_rank", "generate_report")
    workflow.add_edge("generate_report", END)

    return workflow.compile()