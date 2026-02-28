import json
import pandas as pd
from typing import List, Dict, Optional

class DataLoader:
    def __init__(self):
        self.companies_json_path = 'data/companies.json'
        self.companies_csv_path = 'data/companies.csv' 
        self.sector_weights_path = 'data/sector_weights.json'
    
    def load_companies_json(self) -> List[Dict]:
        """Load companies from JSON file."""
        try:
            with open(self.companies_json_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def load_companies_csv(self) -> pd.DataFrame:
        """Load companies from CSV file with additional metadata."""
        try:
            return pd.read_csv(self.companies_csv_path)
        except FileNotFoundError:
            return pd.DataFrame()
    
    def load_sector_weights(self) -> Dict:
        """Load sector weights and multipliers."""
        try:
            with open(self.sector_weights_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"sector_weights": {}, "growth_multipliers": {}}
    
    def get_top_companies(self, limit: int = 20) -> List[Dict]:
        """Get top N companies for analysis."""
        companies = self.load_companies_json()
        return companies[:limit]
    
    def export_results(self, results: List[Dict], filename: str = 'analysis_results.csv'):
        """Export analysis results to CSV."""
        df = pd.DataFrame(results)
        output_path = f'data/output/{filename}'
        df.to_csv(output_path, index=False)
        return output_path