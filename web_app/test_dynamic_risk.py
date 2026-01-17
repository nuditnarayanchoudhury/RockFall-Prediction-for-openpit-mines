#!/usr/bin/env python3
"""
Test script to validate dynamic risk generation
"""

from data_service import DataService
from prediction_service import RockfallPredictor
import time

def test_dynamic_risk_generation():
    print("=== Testing Dynamic Risk Generation ===")
    
    # Initialize services
    data_service = DataService()
    predictor = RockfallPredictor()
    
    # Get all mines
    mines = data_service.get_indian_mines()
    
    print(f"\nTesting {len(mines)} mines for risk distribution...")
    
    risk_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
    mine_risks = []
    
    for mine in mines:
        # Get real-time data
        mine_data = data_service.get_realtime_data(mine['id'])
        
        # Predict risk
        risk_result = predictor.predict_risk(mine_data)
        
        risk_level = risk_result['risk_level']
        risk_score = risk_result['risk_score']
        
        risk_counts[risk_level] += 1
        mine_risks.append({
            'name': mine['name'],
            'location': mine['location'],
            'risk_level': risk_level,
            'risk_score': risk_score,
            'key_factors': risk_result['key_factors'][:3]  # Top 3 factors
        })
        
        print(f"  {mine['name'][:25]:<25} | {risk_level:>6} | {risk_score:.3f}")
    
    print(f"\n=== RISK DISTRIBUTION ===")
    print(f"HIGH RISK:   {risk_counts['HIGH']:>2} mines ({risk_counts['HIGH']/len(mines)*100:.1f}%)")
    print(f"MEDIUM RISK: {risk_counts['MEDIUM']:>2} mines ({risk_counts['MEDIUM']/len(mines)*100:.1f}%)")
    print(f"LOW RISK:    {risk_counts['LOW']:>2} mines ({risk_counts['LOW']/len(mines)*100:.1f}%)")
    
    # Show some high risk mines details
    high_risk_mines = [m for m in mine_risks if m['risk_level'] == 'HIGH']
    if high_risk_mines:
        print(f"\n=== HIGH RISK MINES DETAILS ===")
        for mine in high_risk_mines[:5]:  # Show top 5
            print(f"\n🚨 {mine['name']} - {mine['location']}")
            print(f"   Risk Score: {mine['risk_score']:.3f}")
            print(f"   Key Factors: {', '.join(mine['key_factors'])}")
    
    # Test time-based dynamics by running multiple times
    print(f"\n=== TESTING TIME-BASED DYNAMICS ===")
    print("Testing same mine multiple times to show variation...")
    
    test_mine = mines[0]  # Use first mine
    for i in range(5):
        mine_data = data_service.get_realtime_data(test_mine['id'])
        risk_result = predictor.predict_risk(mine_data)
        print(f"Test {i+1}: {test_mine['name'][:20]:<20} | {risk_result['risk_level']:>6} | {risk_result['risk_score']:.3f}")
        time.sleep(1)  # Small delay to show time-based variation
    
    return risk_counts

if __name__ == "__main__":
    risk_counts = test_dynamic_risk_generation()
    
    # Success criteria
    total_mines = sum(risk_counts.values())
    high_percentage = risk_counts['HIGH'] / total_mines * 100
    medium_percentage = risk_counts['MEDIUM'] / total_mines * 100
    
    print(f"\n=== TEST RESULTS ===")
    if high_percentage >= 10 and medium_percentage >= 15:
        print("✅ SUCCESS: Realistic risk distribution achieved!")
        print(f"   HIGH: {high_percentage:.1f}% (target: ≥10%)")
        print(f"   MEDIUM: {medium_percentage:.1f}% (target: ≥15%)")
    else:
        print("❌ NEEDS IMPROVEMENT: Risk distribution too low")
        print(f"   HIGH: {high_percentage:.1f}% (target: ≥10%)")  
        print(f"   MEDIUM: {medium_percentage:.1f}% (target: ≥15%)")