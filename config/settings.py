import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Set your API Key
os.environ["GOOGLE_API_KEY"] = "ABCD"


# Prompt for moat analysis
MOAT_PROMPT = ChatPromptTemplate.from_template("""
You are a Senior Equity Research Analyst. Your task is to score the 'Moat' of a company
contributing to the AI Factory Capital Stack.

Company: {company_name}
Sector: {sector}

Criteria for Moat Score (0-5):
1. Architectural lock-in (e.g., proprietary standards like CUDA)
2. Ecosystem dominance (design wins, reference architectures)
3. Switching costs / standard-setting influence
4. Scarcity or bottleneck position in the supply chain

Analysis Task:
- Briefly describe the company's differentiation in the AI Factory ecosystem.
- Assign a Moat Score from 0 to 5 based on the criteria above.

Return ONLY a JSON object in this format:
{{
  "moat_score": integer,
  "narrative": "string summary"
}}
""")

# Initialize the model
def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2
    )