import json
from utils.workflow import create_workflow

def load_companies():
    """Load companies data from JSON file."""
    with open('data/companies.json', 'r') as f:
        return json.load(f)

def main():
    """Main entry point to run the ranking analysis."""
    print("Creating LangGraph workflow...")
    app = create_workflow()
    print("Workflow compiled successfully.")
    
    companies = load_companies()
    results = []

    for co in companies:
        print(f"\nRunning analysis for {co['company_name']}...")
        output = app.invoke(co)
        results.append(output)

    # Sort by the TAFGS score (Highest to Lowest)
    ranked_list = sorted(results, key=lambda x: x['final_score'], reverse=True)
    
    print("\n" + "="*60)
    print("TOP COMPANIES RANKING (TAFGS Score)")
    print("="*60)
    
    for rank, item in enumerate(ranked_list, 1):
        print(f"{rank}. {item['company_name']}")
        print(f"   Score: {item['final_score']:.2f}")
        print(f"   Moat Summary: {item['report_summary']}")
        print("-" * 40)

if __name__ == "__main__":
    main()