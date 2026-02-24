from state import AgentState

def ranking_agent(state: AgentState):
    """Computes Total AI Factory Growth Score."""
    final = (state['moat_score'] * state['margin_score']) * state['growth_forecast']
    return {"final_score": final}