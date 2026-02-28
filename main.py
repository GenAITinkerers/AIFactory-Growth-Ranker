# main.py - Enhanced version
import json
import sys
import argparse
from utils.workflow import create_workflow
from utils.data_loader import DataLoader
from utils.analysis_engine import AnalysisEngine

def main():
    parser = argparse.ArgumentParser(description='AI Factory Growth Ranker')
    parser.add_argument('--mode', choices=['cli', 'streamlit', 'top20'], 
                       default='cli', help='Run mode')
    parser.add_argument('--limit', type=int, default=20, 
                       help='Number of companies to analyze')
    parser.add_argument('--export', action='store_true', 
                       help='Export results to CSV')
    
    args = parser.parse_args()
    
    if args.mode == 'streamlit':
        import subprocess
        subprocess.run(["streamlit", "run", "streamlit_app.py"])
        return
    
    # Initialize components
    engine = AnalysisEngine()
    data_loader = DataLoader()
    
    print(f"🏭 AI Factory Growth Ranker - Analyzing Top {args.limit} Companies")
    print("=" * 60)
    
    # Load companies
    companies = data_loader.get_top_companies(args.limit)
    
    if not companies:
        print("❌ No company data found. Please check data/companies.json")
        return
    
    print(f"📊 Found {len(companies)} companies to analyze...")
    
    # Run analysis
    results = engine.analyze_batch(companies)
    
    # Get rankings
    rankings = engine.get_top_rankings(results, args.limit)
    
    # Display results
    print(f"\n🏆 TOP {len(rankings)} AI FACTORY COMPANIES")
    print("=" * 60)
    
    for rank, company in enumerate(rankings, 1):
        print(f"{rank:2d}. {company['company_name']:25s} "
              f"Score: {company.get('final_score', 0):7.2f} "
              f"Sector: {company.get('sector', 'N/A')}")
        if company.get('report_summary'):
            print(f"    📝 {company['report_summary'][:100]}...")
        print("-" * 60)
    
    # Sector analysis
    sector_stats = engine.generate_sector_analysis(rankings)
    print(f"\n📊 SECTOR ANALYSIS")
    print("=" * 40)
    for sector, stats in sector_stats.items():
        print(f"{sector:25s} Companies: {stats['count']:2d} "
              f"Avg Score: {stats['avg_score']:6.2f}")
    
    # Export if requested
    if args.export:
        output_file = data_loader.export_results(rankings, 
                                                f'top_{args.limit}_rankings.csv')
        print(f"\n📁 Results exported to: {output_file}")

if __name__ == "__main__":
    main()