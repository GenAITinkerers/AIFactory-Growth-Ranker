import json
from state import AgentState
from config.settings import MOAT_PROMPT, get_llm

def moat_analysis_agent(state: AgentState):
    """The Moat Specialist Agent 'thinks' about defensibility."""
    llm = get_llm()
    chain = MOAT_PROMPT | llm
    response = chain.invoke({
        "company_name": state["company_name"],
        "sector": state["sector"]
    })

    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        cleaned_content = response.content.strip().replace('```json', '').replace('```', '')
        try:
            result = json.loads(cleaned_content)
        except json.JSONDecodeError:
            return {"moat_score": 0, "report_summary": "LLM failed to return valid JSON."}

    return {
        "moat_score": result["moat_score"],
        "report_summary": result["narrative"]
    }