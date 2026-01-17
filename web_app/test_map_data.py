#!/usr/bin/env python3
"""
Diagnostic script to test map data loading and identify issues
"""

import sys
import json
from data_service import DataService
from prediction_service import RockfallPredictor

def test_data_loading():
    """Test if data services are working properly"""
    print("=" * 60)
    print("DIAGNOSTIC TEST: Map Data Loading")
    print("=" * 60)
    
    # Initialize services
    print("\n1. Initializing services...")
    try:
        data_service = DataService()
        predictor = RockfallPredictor()
        print("   ✓ Services initialized successfully")
    except Exception as e:
        print(f"   ✗ Failed to initialize services: {e}")
        return False
    
    # Test mine data loading
    print("\n2. Testing mine data loading...")
    try:
        mines = data_service.get_indian_mines()
        print(f"   ✓ Loaded {len(mines)} mines")
        
        if len(mines) == 0:
            print("   ✗ WARNING: No mines loaded!")
            return False
            
        # Show sample mine data
        sample_mine = mines[0]
        print(f"\n   Sample Mine Data:")
        print(f"   - ID: {sample_mine['id']}")
        print(f"   - Name: {sample_mine['name']}")
        print(f"   - Coordinates: {sample_mine['coordinates']}")
        print(f"   - State: {sample_mine['state']}")
        
    except Exception as e:
        print(f"   ✗ Failed to load mines: {e}")
        return False
    
    # Test predictions for each mine
    print("\n3. Testing predictions for all mines...")
    predictions = []
    failed_count = 0
    
    for i, mine in enumerate(mines, 1):
        try:
            # Get real-time data
            mine_data = data_service.get_realtime_data(mine['id'])
            
            # Make prediction
            risk_data = predictor.predict_risk(mine_data)
            
            prediction = {
                'mine_id': mine['id'],
                'mine_name': mine['name'],
                'location': mine['location'],
                'coordinates': mine['coordinates'],
                'risk_level': risk_data['risk_level'],
                'risk_score': risk_data['risk_score'],
                'confidence': risk_data['confidence']
            }
            predictions.append(prediction)
            
            status_symbol = {
                'HIGH': '🔴',
                'MEDIUM': '🟡',
                'LOW': '🟢'
            }.get(risk_data['risk_level'], '⚪')
            
            print(f"   {status_symbol} Mine {i:2d}/{len(mines)}: {mine['name'][:30]:<30} | Risk: {risk_data['risk_level']:<6} | Score: {risk_data['risk_score']:.3f}")
            
        except Exception as e:
            failed_count += 1
            print(f"   ✗ Mine {i:2d}/{len(mines)}: {mine['name'][:30]:<30} | FAILED: {str(e)[:50]}")
    
    print(f"\n   Summary: {len(predictions)} successful, {failed_count} failed")
    
    # Test coordinate format
    print("\n4. Validating coordinate format...")
    invalid_coords = []
    for pred in predictions:
        coords = pred['coordinates']
        if not isinstance(coords, list) or len(coords) != 2:
            invalid_coords.append(pred['mine_name'])
        elif not (-90 <= coords[0] <= 90) or not (-180 <= coords[1] <= 180):
            invalid_coords.append(pred['mine_name'])
    
    if invalid_coords:
        print(f"   ✗ Found {len(invalid_coords)} mines with invalid coordinates:")
        for name in invalid_coords[:5]:
            print(f"      - {name}")
    else:
        print(f"   ✓ All coordinates are valid")
    
    # Generate sample JSON output
    print("\n5. Sample JSON output (first 3 mines):")
    sample_json = json.dumps(predictions[:3], indent=2)
    print(sample_json)
    
    # Risk distribution
    print("\n6. Risk Distribution:")
    risk_stats = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
    for pred in predictions:
        risk_level = pred.get('risk_level', 'UNKNOWN')
        if risk_level in risk_stats:
            risk_stats[risk_level] += 1
    
    print(f"   🔴 HIGH Risk:   {risk_stats['HIGH']:2d} mines")
    print(f"   🟡 MEDIUM Risk: {risk_stats['MEDIUM']:2d} mines")
    print(f"   🟢 LOW Risk:    {risk_stats['LOW']:2d} mines")
    
    # Map bounds
    print("\n7. Map Bounds (for debugging map view):")
    all_lats = [p['coordinates'][0] for p in predictions]
    all_lons = [p['coordinates'][1] for p in predictions]
    print(f"   Latitude range:  {min(all_lats):.4f} to {max(all_lats):.4f}")
    print(f"   Longitude range: {min(all_lons):.4f} to {max(all_lons):.4f}")
    print(f"   Suggested center: [{sum(all_lats)/len(all_lats):.4f}, {sum(all_lons)/len(all_lons):.4f}]")
    
    print("\n" + "=" * 60)
    print("✓ DIAGNOSTIC TEST COMPLETED SUCCESSFULLY")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    try:
        success = test_data_loading()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
