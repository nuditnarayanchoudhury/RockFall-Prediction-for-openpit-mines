#!/usr/bin/env python3
"""
Test alert generation
"""

from data_service import DataService
from prediction_service import RockfallPredictor

data_service = DataService()
predictor = RockfallPredictor()

print('=== CHECKING ALERT GENERATION ===')
mines = data_service.get_indian_mines()
alerts = []

for mine in mines[:5]:  # Test first 5 mines
    mine_data = data_service.get_realtime_data(mine['id'])
    risk_result = predictor.predict_risk(mine_data)
    
    if risk_result['risk_level'] in ['HIGH', 'MEDIUM']:
        name = mine['name'][:25]
        level = risk_result['risk_level']
        score = risk_result['risk_score']
        factors = risk_result['key_factors'][:2]
        
        print(f'{name:<25} | {level:>6} | {score:.3f}')
        print(f'  Factors: {factors}')
        print()