from state import AgentState

def report_agent(state: AgentState):
    """Produces investor-ready output."""
    summary = f"Ranked Profile for {state['company_name']}: Score {state['final_score']}. Moat Summary: {state['report_summary']}"
    return {"report": summary}