#!/usr/bin/env python3
"""
Test script to verify all system components work correctly
"""

import sys
import os

# Import services at module level
try:
    from data_service import DataService
    from prediction_service import RockfallPredictor
    from alert_service import AlertService
except ImportError as e:
    print(f"Warning: Could not import services: {e}")
    DataService = None
    RockfallPredictor = None
    AlertService = None

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import flask
        print("✓ Flask imported successfully")
    except ImportError as e:
        print(f"✗ Flask import failed: {e}")
        return False
        
    try:
        import pandas as pd
        print("✓ Pandas imported successfully")
    except ImportError as e:
        print(f"✗ Pandas import failed: {e}")
        return False
        
    try:
        import numpy as np
        print("✓ NumPy imported successfully")  
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
        
    try:
        from data_service import DataService
        print("✓ DataService imported successfully")
    except ImportError as e:
        print(f"✗ DataService import failed: {e}")
        return False
        
    try:
        from prediction_service import RockfallPredictor
        print("✓ RockfallPredictor imported successfully")
    except ImportError as e:
        print(f"✗ RockfallPredictor import failed: {e}")
        return False
        
    try:
        from alert_service import AlertService
        print("✓ AlertService imported successfully")
    except ImportError as e:
        print(f"✗ AlertService import failed: {e}")
        return False
    
    return True

def test_data_service():
    """Test DataService functionality"""
    print("\nTesting DataService...")
    
    if DataService is None:
        print("✗ DataService not available")
        return False
    
    try:
        data_service = DataService()
        mines = data_service.get_indian_mines()
        print(f"✓ Loaded {len(mines)} Indian mines")
        
        # Test getting a specific mine
        mine = data_service.get_mine_by_id('mine_001')
        if mine:
            print(f"✓ Retrieved mine: {mine['name']}")
        else:
            print("✗ Failed to retrieve specific mine")
            return False
            
        # Test real-time data generation
        realtime_data = data_service.get_realtime_data('mine_001')
        if realtime_data and 'timestamp' in realtime_data:
            print("✓ Generated real-time data successfully")
        else:
            print("✗ Failed to generate real-time data")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ DataService test failed: {e}")
        return False

def test_prediction_service():
    """Test PredictionService functionality"""
    print("\nTesting PredictionService...")
    
    if RockfallPredictor is None:
        print("✗ RockfallPredictor not available")
        return False
    
    try:
        predictor = RockfallPredictor()
        print("✓ RockfallPredictor initialized")
        
        # Test with sample data
        sample_data = {
            'latitude': 23.7644,
            'longitude': 86.4084,
            'elevation': 250,
            'slope': 35.5,
            'earthquake_magnitude': 3.2,
            'rainfall_jul': 180.5,
            'displacement': 2.1,
            'strain': 45.0,
            'pore_pressure': 120.0,
            'seismic_vibration': 5.2,
            'crack_density': 0.023
        }
        
        result = predictor.predict_risk(sample_data)
        if result and 'risk_level' in result:
            print(f"✓ Prediction successful: {result['risk_level']} (score: {result['risk_score']:.3f})")
        else:
            print("✗ Prediction failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ PredictionService test failed: {e}")
        return False

def test_alert_service():
    """Test AlertService functionality"""
    print("\nTesting AlertService...")
    
    if AlertService is None:
        print("✗ AlertService not available")
        return False
    
    try:
        alert_service = AlertService()
        print("✓ AlertService initialized")
        
        # Test getting active alerts
        alerts = alert_service.get_active_alerts()
        print(f"✓ Retrieved {len(alerts)} active alerts")
        
        # Test alert statistics
        stats = alert_service.get_alert_statistics()
        if stats and 'total_alerts' in stats:
            print(f"✓ Alert statistics generated: {stats['total_alerts']} total alerts")
        else:
            print("✗ Failed to generate alert statistics")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ AlertService test failed: {e}")
        return False

def test_integration():
    """Test integration between services"""
    print("\nTesting service integration...")
    
    if None in [DataService, RockfallPredictor, AlertService]:
        print("✗ Some services not available for integration test")
        return False
    
    try:
        # Initialize services
        data_service = DataService()
        predictor = RockfallPredictor()
        alert_service = AlertService()
        
        # Get a mine and its data
        mine = data_service.get_mine_by_id('mine_001')
        realtime_data = data_service.get_realtime_data('mine_001')
        
        # Make prediction
        prediction = predictor.predict_risk(realtime_data)
        
        # Check if alert would be triggered
        if prediction['risk_level'] in ['HIGH', 'MEDIUM']:
            print(f"✓ Integration test: {mine['name']} has {prediction['risk_level']} risk - alert would be triggered")
        else:
            print(f"✓ Integration test: {mine['name']} has {prediction['risk_level']} risk - normal operation")
            
        return True
        
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== AI Rockfall Prediction System - Component Test ===\n")
    
    tests = [
        test_imports,
        test_data_service,
        test_prediction_service,
        test_alert_service,
        test_integration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! System is ready to run.")
        return True
    else:
        print(f"\n❌ {failed} test(s) failed. Please fix the issues before running the system.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
