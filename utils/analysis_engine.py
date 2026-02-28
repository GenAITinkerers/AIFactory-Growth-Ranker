import asyncio
from typing import List, Dict
from utils.workflow import create_workflow
from utils.data_loader import DataLoader
import time

class AnalysisEngine:
    def __init__(self):
        self.workflow = create_workflow()
        self.data_loader = DataLoader()
        
    def analyze_single_company(self, company: Dict) -> Dict:
        """Analyze a single company."""
        try:
            result = self.workflow.invoke(company)
            result['timestamp'] = time.time()
            return result
        except Exception as e:
            return {
                'company_name': company.get('company_name', 'Unknown'),
                'error': str(e),
                'final_score': 0,
                'timestamp': time.time()
            }
    
    def analyze_batch(self, companies: List[Dict]) -> List[Dict]:
        """Analyze multiple companies in sequence."""
        results = []
        for i, company in enumerate(companies):
            print(f"Analyzing {i+1}/{len(companies)}: {company['company_name']}")
            result = self.analyze_single_company(company)
            results.append(result)
            time.sleep(0.5)  # Rate limiting
        return results
    
    def get_top_rankings(self, results: List[Dict], limit: int = 20) -> List[Dict]:
        """Get top N companies by TAFGS score."""
        valid_results = [r for r in results if 'error' not in r]
        ranked = sorted(valid_results, key=lambda x: x.get('final_score', 0), reverse=True)
        return ranked[:limit]
    
    def generate_sector_analysis(self, results: List[Dict]) -> Dict:
        """Generate sector-wise analysis."""
        sector_stats = {}
        for result in results:
            sector = result.get('sector', 'Unknown')
            if sector not in sector_stats:
                sector_stats[sector] = {
                    'companies': [],
                    'avg_score': 0,
                    'count': 0,
                    'top_score': 0
                }
            
            sector_stats[sector]['companies'].append(result['company_name'])
            sector_stats[sector]['count'] += 1
            score = result.get('final_score', 0)
            if score > sector_stats[sector]['top_score']:
                sector_stats[sector]['top_score'] = score
        
        # Calculate averages
        for sector in sector_stats:
            if sector_stats[sector]['count'] > 0:
                total_score = sum(r.get('final_score', 0) for r in results if r.get('sector') == sector)
                sector_stats[sector]['avg_score'] = total_score / sector_stats[sector]['count']
        
        return sector_stats