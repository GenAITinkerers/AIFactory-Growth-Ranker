from state import AgentState

def margin_analysis_agent(state: AgentState):
    """Normalizes operating margin strength."""
    margin = state['operating_margin']
    if margin > 0.40: 
        score = 5
    elif margin > 0.30: 
        score = 4
    elif margin > 0.20: 
        score = 3
    elif margin > 0.10: 
        score = 2
    else: 
        score = 1
    return {"margin_score": score}