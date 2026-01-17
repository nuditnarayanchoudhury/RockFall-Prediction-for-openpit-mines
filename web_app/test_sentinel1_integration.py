#!/usr/bin/env python3
"""
Test script for Sentinel-1 integration with the rockfall prediction system
"""

from data_service import DataService
from prediction_service import RockfallPredictor
import json

def test_sentinel1_integration():
    print("=" * 60)
    print("🛰️  Testing Sentinel-1 SAR Data Integration")
    print("=" * 60)
    
    # Initialize services
    data_service = DataService()
    predictor = RockfallPredictor()
    
    # Test all 18 mining locations
    mines = data_service.get_indian_mines()
    
    print(f"Testing {len(mines)} mining locations with Sentinel-1 data...")
    print()
    
    high_risk_mines = []
    medium_risk_mines = []
    low_risk_mines = []
    
    for i, mine in enumerate(mines[:5], 1):  # Test first 5 mines for demo
        print(f"{i}. Testing {mine['name']} ({mine['location']})...")
        
        # Get real-time data (now includes Sentinel-1 features)
        mine_data = data_service.get_realtime_data(mine['id'])
        
        # Check if SAR features are present
        sar_features = [k for k in mine_data.keys() if k.startswith('sar_')]
        has_sar_data = len(sar_features) > 0
        
        print(f"   📡 SAR Features: {len(sar_features)} features available")
        if has_sar_data:
            print(f"   📊 SAR Displacement: {mine_data.get('sar_displacement_mm', 0):.2f} mm")
            print(f"   📊 SAR Coherence: {mine_data.get('sar_coherence', 0):.3f}")
            print(f"   📊 SAR Data Quality: {mine_data.get('sar_data_quality', 0):.3f}")
        
        # Make prediction with enhanced SAR features
        prediction = predictor.predict_risk(mine_data)
        
        print(f"   🎯 Risk Level: {prediction['risk_level']}")
        print(f"   📈 Risk Score: {prediction['risk_score']:.3f}")
        print(f"   🔍 Confidence: {prediction['confidence']:.3f}")
        
        # Show SAR-related risk factors
        sar_factors = [f for f in prediction['key_factors'] if 'SAR' in f or 'coherence' in f or 'decorrelation' in f]
        if sar_factors:
            print(f"   🛰️  SAR Risk Factors: {sar_factors}")
        
        # Categorize mines by risk
        if prediction['risk_level'] == 'HIGH':
            high_risk_mines.append(mine['name'])
        elif prediction['risk_level'] == 'MEDIUM':
            medium_risk_mines.append(mine['name'])
        else:
            low_risk_mines.append(mine['name'])
        
        print()
    
    # Summary
    print("=" * 60)
    print("📊 RISK ASSESSMENT SUMMARY")
    print("=" * 60)
    print(f"🔴 HIGH RISK ({len(high_risk_mines)}): {', '.join(high_risk_mines) if high_risk_mines else 'None'}")
    print(f"🟡 MEDIUM RISK ({len(medium_risk_mines)}): {', '.join(medium_risk_mines) if medium_risk_mines else 'None'}")
    print(f"🟢 LOW RISK ({len(low_risk_mines)}): {', '.join(low_risk_mines) if low_risk_mines else 'None'}")
    print()
    
    # Test specific SAR data integration
    print("=" * 60)
    print("🧪 DETAILED SAR FEATURE ANALYSIS")
    print("=" * 60)
    
    test_mine = mines[0]  # Jharia Coalfield
    print(f"Detailed analysis for: {test_mine['name']}")
    
    mine_data = data_service.get_realtime_data(test_mine['id'])
    
    # Display SAR features
    sar_data = {}
    for key, value in mine_data.items():
        if key.startswith('sar_'):
            sar_data[key] = value
    
    if sar_data:
        print("\n🛰️  Sentinel-1 SAR Features:")
        for feature, value in sar_data.items():
            if isinstance(value, (int, float)):
                print(f"   {feature}: {value:.4f}")
            else:
                print(f"   {feature}: {value}")
    else:
        print("   ⚠️  No SAR features found in data")
    
    print("\n✅ Sentinel-1 integration test completed!")

if __name__ == "__main__":
    test_sentinel1_integration()