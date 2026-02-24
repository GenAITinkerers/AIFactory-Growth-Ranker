from typing import TypedDict

class AgentState(TypedDict):
    company_name: str
    sector: str
    operating_margin: float
    moat_score: int
    growth_forecast: float
    final_score: float
    report: str
    margin_score: int
    report_summary: str