#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_service import DataService
from prediction_service import RockfallPredictor

def test_geological_risk_distribution():
    """Test the geological-based risk distribution"""
    print("Testing Geological-Based Risk Distribution")
    print("=" * 50)
    
    # Initialize services
    data_service = DataService()
    risk_service = RockfallPredictor()
    
    # Get all mines
    mines = data_service.get_indian_mines()
    
    risk_counts = {'LOW': 0, 'MEDIUM': 0, 'HIGH': 0}
    mine_results = []
    
    print("\nProcessing all mines...")
    for mine in mines:
        result = risk_service.predict_risk(mine)
        risk_level = result['risk_level']
        risk_counts[risk_level] += 1
        
        mine_results.append({
            'mine_id': mine['id'],
            'name': mine['name'],
            'risk_level': risk_level,
            'risk_score': result['risk_score'],
            'key_factors': result.get('key_factors', []),
            'xai_explanation': result.get('xai_explanation', 'N/A')
        })
    
    # Print summary
    total_mines = len(mines)
    print(f"\n📊 RISK DISTRIBUTION SUMMARY:")
    print(f"Total Mines: {total_mines}")
    print(f"LOW Risk:    {risk_counts['LOW']:2d} ({risk_counts['LOW']/total_mines*100:.1f}%)")
    print(f"MEDIUM Risk: {risk_counts['MEDIUM']:2d} ({risk_counts['MEDIUM']/total_mines*100:.1f}%)")
    print(f"HIGH Risk:   {risk_counts['HIGH']:2d} ({risk_counts['HIGH']/total_mines*100:.1f}%)")
    
    # Print detailed mine assignments
    print(f"\n🏔️  DETAILED MINE RISK ASSIGNMENTS:")
    print("-" * 80)
    
    for category in ['HIGH', 'MEDIUM', 'LOW']:
        category_mines = [m for m in mine_results if m['risk_level'] == category]
        if category_mines:
            print(f"\n{category} RISK MINES ({len(category_mines)}):")
            for mine in category_mines:
                print(f"  • {mine['mine_id']:8} | {mine['name'][:30]:30} | Score: {mine['risk_score']:.3f}")
                factors_str = ", ".join(mine['key_factors'][:3])
                print(f"    Key Factors: {factors_str}")
    
    # Expected distribution check
    print(f"\n✅ GEOLOGICAL DISTRIBUTION ANALYSIS:")
    expected_high = 5  # Designated high-risk mines
    expected_medium = 4  # Designated medium-risk mines
    expected_low_base = 10  # All other mines as base low-risk
    
    print(f"Expected HIGH risk mines: ~{expected_high} (with some variation)")
    print(f"Expected MEDIUM risk mines: ~{expected_medium} (with some variation)")
    print(f"Expected LOW risk mines: ~{expected_low_base} (with some variation)")
    
    if risk_counts['HIGH'] >= 3 and risk_counts['MEDIUM'] >= 2:
        print("✅ Distribution looks good - proper spread across risk levels")
    else:
        print("⚠️  Distribution may need adjustment")
    
    return mine_results, risk_counts

def test_multiple_runs():
    """Test multiple runs to check consistency"""
    print("\n" + "="*50)
    print("TESTING CONSISTENCY ACROSS MULTIPLE RUNS")
    print("="*50)
    
    run_results = []
    for i in range(5):
        print(f"\nRun {i+1}:")
        _, counts = test_geological_risk_distribution()
        run_results.append(counts)
        print(f"  LOW: {counts['LOW']}, MEDIUM: {counts['MEDIUM']}, HIGH: {counts['HIGH']}")
    
    print(f"\n📈 CONSISTENCY ANALYSIS:")
    avg_low = sum(r['LOW'] for r in run_results) / len(run_results)
    avg_medium = sum(r['MEDIUM'] for r in run_results) / len(run_results)
    avg_high = sum(r['HIGH'] for r in run_results) / len(run_results)
    
    print(f"Average LOW: {avg_low:.1f}")
    print(f"Average MEDIUM: {avg_medium:.1f}")
    print(f"Average HIGH: {avg_high:.1f}")

if __name__ == "__main__":
    try:
        mine_results, risk_counts = test_geological_risk_distribution()
        
        # Optionally run multiple tests
        user_input = input("\nWould you like to test consistency across multiple runs? (y/n): ").strip().lower()
        if user_input == 'y':
            test_multiple_runs()
            
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()