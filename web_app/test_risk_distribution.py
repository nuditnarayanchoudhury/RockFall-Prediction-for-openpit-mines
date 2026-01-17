#!/usr/bin/env python3
"""
Test script to show detailed risk distribution across all mining locations
"""

from data_service import DataService
from prediction_service import RockfallPredictor

def test_risk_distribution():
    print("🎯 TESTING RISK DISTRIBUTION ACROSS ALL MINES")
    print("=" * 60)
    
    # Initialize services
    ds = DataService()
    pred = RockfallPredictor()
    
    # Get all mines
    mines = ds.get_indian_mines()
    results = []
    
    print("Processing risk predictions for all mines...\n")
    
    for mine in mines:
        try:
            data = ds.get_realtime_data(mine['id'])
            risk = pred.predict_risk(data)
            results.append({
                'name': mine['name'],
                'location': mine['location'],
                'state': mine['state'],
                'type': mine['type'],
                'risk_level': risk['risk_level'],
                'risk_score': risk['risk_score'],
                'confidence': risk['confidence'],
                'factors': risk.get('key_factors', [])
            })
        except Exception as e:
            print(f"Error processing {mine['name']}: {e}")
            continue
    
    # Categorize results
    high_risk = [r for r in results if r['risk_level'] == 'HIGH']
    medium_risk = [r for r in results if r['risk_level'] == 'MEDIUM']
    low_risk = [r for r in results if r['risk_level'] == 'LOW']
    
    print("📊 RISK DISTRIBUTION SUMMARY:")
    print(f"🔴 HIGH RISK: {len(high_risk)} mines")
    print(f"🟡 MEDIUM RISK: {len(medium_risk)} mines")
    print(f"🟢 LOW RISK: {len(low_risk)} mines")
    print()
    
    if high_risk:
        print("🔴 HIGH RISK MINES:")
        for mine in high_risk:
            print(f"  • {mine['name']} ({mine['location']})")
            print(f"    Risk Score: {mine['risk_score']:.3f} | Confidence: {mine['confidence']:.3f}")
            print(f"    Type: {mine['type']} | State: {mine['state']}")
            if mine['factors']:
                print(f"    Key Factors: {', '.join(mine['factors'][:3])}")
            print()
    else:
        print("🔴 No mines currently at HIGH risk")
        print()
    
    if medium_risk:
        print("🟡 MEDIUM RISK MINES:")
        for mine in medium_risk:
            print(f"  • {mine['name']} ({mine['location']})")
            print(f"    Risk Score: {mine['risk_score']:.3f} | Confidence: {mine['confidence']:.3f}")
            print(f"    Type: {mine['type']} | State: {mine['state']}")
            if mine['factors']:
                print(f"    Key Factors: {', '.join(mine['factors'][:3])}")
            print()
    else:
        print("🟡 No mines currently at MEDIUM risk")
        print()
    
    print(f"🟢 LOW RISK MINES: {len(low_risk)} mines operating normally")
    
    # Show risk score distribution
    print("\n📈 RISK SCORE STATISTICS:")
    risk_scores = [r['risk_score'] for r in results]
    print(f"   Highest Risk Score: {max(risk_scores):.3f}")
    print(f"   Lowest Risk Score: {min(risk_scores):.3f}")
    print(f"   Average Risk Score: {sum(risk_scores)/len(risk_scores):.3f}")
    
    # Show by state
    print("\n🌍 RISK DISTRIBUTION BY STATE:")
    states = {}
    for result in results:
        state = result['state']
        if state not in states:
            states[state] = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        states[state][result['risk_level']] += 1
    
    for state, counts in sorted(states.items()):
        total = sum(counts.values())
        print(f"  {state}: {total} mines (H:{counts['HIGH']}, M:{counts['MEDIUM']}, L:{counts['LOW']})")
    
    print("\n✅ Risk distribution analysis complete!")

if __name__ == "__main__":
    test_risk_distribution()