#!/usr/bin/env python3
"""
Quick test to show randomized risk distribution
"""

from data_service import DataService
from prediction_service import RockfallPredictor

def quick_test():
    # Initialize services
    data_service = DataService()
    predictor = RockfallPredictor()
    
    print("=== QUICK RANDOMIZED RISK TEST ===")
    print("Running 3 tests to show different distributions each time...\n")
    
    for test_num in range(1, 4):
        print(f"--- Test {test_num} ---")
        
        # Get mines
        mines = data_service.get_indian_mines()
        
        risk_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        
        for mine in mines:
            mine_data = data_service.get_realtime_data(mine['id'])
            risk_result = predictor.predict_risk(mine_data)
            risk_counts[risk_result['risk_level']] += 1
        
        total = sum(risk_counts.values())
        print(f"HIGH:   {risk_counts['HIGH']:2d} mines ({risk_counts['HIGH']/total*100:.1f}%)")
        print(f"MEDIUM: {risk_counts['MEDIUM']:2d} mines ({risk_counts['MEDIUM']/total*100:.1f}%)")
        print(f"LOW:    {risk_counts['LOW']:2d} mines ({risk_counts['LOW']/total*100:.1f}%)")
        print()

if __name__ == "__main__":
    quick_test()