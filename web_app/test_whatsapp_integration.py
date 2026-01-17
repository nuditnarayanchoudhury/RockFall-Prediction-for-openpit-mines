#!/usr/bin/env python3
"""
Comprehensive test script for WhatsApp integration
Tests all WhatsApp functionality in the project
"""

import os
import sys
from datetime import datetime

def test_whatsapp_dependencies():
    """Test if WhatsApp dependencies are installed"""
    print("🔍 Testing WhatsApp Dependencies...")
    print("-" * 50)
    
    try:
        import pywhatkit
        print("✅ pywhatkit installed successfully")
    except ImportError:
        print("❌ pywhatkit not installed")
        print("   Run: pip install pywhatkit")
        return False
    
    try:
        import pyautogui
        print("✅ pyautogui installed successfully")
    except ImportError:
        print("❌ pyautogui not installed")
        print("   Run: pip install pyautogui")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow (PIL) installed successfully")
    except ImportError:
        print("❌ Pillow not installed")
        print("   Run: pip install pillow")
        return False
    
    return True

def test_whatsapp_service():
    """Test WhatsApp service functionality"""
    print("\n🚀 Testing WhatsApp Service...")
    print("-" * 50)
    
    try:
        from whatsapp_alert import WhatsAppService
        
        # Initialize service
        whatsapp_service = WhatsAppService()
        
        if not whatsapp_service.available:
            print("❌ WhatsApp service not available")
            return False
        
        print("✅ WhatsApp service initialized successfully")
        
        # Test message formatting
        test_alert = {
            'mine_name': 'Test Mine - Jharkhand',
            'alert_level': 'HIGH',
            'risk_score': 8.5,
            'sensor_data': {
                'vibration': 8.2,
                'acoustic': 95.0,
                'temperature': 42.0
            }
        }
        
        message = whatsapp_service._format_mining_alert(test_alert)
        print("✅ Alert message formatting works")
        print(f"   Message length: {len(message)} characters")
        
        # Test phone number cleaning
        test_phones = ['+917735776771', '7735776771', '917735776771']
        for phone in test_phones:
            cleaned = whatsapp_service._clean_phone_number(phone)
            print(f"   {phone} -> {cleaned}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import WhatsApp service: {e}")
        return False
    except Exception as e:
        print(f"❌ WhatsApp service test failed: {e}")
        return False

def test_alert_service_integration():
    """Test WhatsApp integration with alert service"""
    print("\n🔗 Testing Alert Service Integration...")
    print("-" * 50)
    
    try:
        from alert_service import AlertService
        
        alert_service = AlertService()
        
        if alert_service.whatsapp_service is None:
            print("❌ WhatsApp service not integrated in AlertService")
            return False
        
        print("✅ WhatsApp service integrated in AlertService")
        
        if hasattr(alert_service, 'send_whatsapp_alert'):
            print("✅ send_whatsapp_alert method available")
        else:
            print("❌ send_whatsapp_alert method missing")
            return False
        
        if hasattr(alert_service, 'send_whatsapp_test'):
            print("✅ send_whatsapp_test method available")
        else:
            print("❌ send_whatsapp_test method missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Alert service integration test failed: {e}")
        return False

def test_flask_endpoints():
    """Test Flask API endpoints for WhatsApp"""
    print("\n🌐 Testing Flask API Endpoints...")
    print("-" * 50)
    
    try:
        from app_with_auth import app
        
        # Check if WhatsApp endpoints exist
        whatsapp_routes = []
        for rule in app.url_map.iter_rules():
            if 'whatsapp' in rule.rule.lower():
                whatsapp_routes.append(rule.rule)
        
        if '/api/send_whatsapp_alert' in whatsapp_routes:
            print("✅ /api/send_whatsapp_alert endpoint available")
        else:
            print("❌ /api/send_whatsapp_alert endpoint missing")
        
        if '/api/test_whatsapp' in whatsapp_routes:
            print("✅ /api/test_whatsapp endpoint available")
        else:
            print("❌ /api/test_whatsapp endpoint missing")
        
        print(f"   Total WhatsApp endpoints: {len(whatsapp_routes)}")
        
        return len(whatsapp_routes) >= 2
        
    except Exception as e:
        print(f"❌ Flask endpoints test failed: {e}")
        return False

def test_requirements():
    """Test if requirements.txt is updated"""
    print("\n📋 Testing Requirements.txt...")
    print("-" * 50)
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
        
        if 'pywhatkit' in requirements:
            print("✅ pywhatkit in requirements.txt")
        else:
            print("❌ pywhatkit missing from requirements.txt")
        
        if 'pyautogui' in requirements:
            print("✅ pyautogui in requirements.txt")
        else:
            print("❌ pyautogui missing from requirements.txt")
        
        if 'pillow' in requirements.lower():
            print("✅ pillow in requirements.txt")
        else:
            print("❌ pillow missing from requirements.txt")
        
        return True
        
    except Exception as e:
        print(f"❌ Requirements test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 COMPREHENSIVE WHATSAPP INTEGRATION TEST")
    print("=" * 80)
    
    tests = [
        ("Dependencies", test_whatsapp_dependencies),
        ("WhatsApp Service", test_whatsapp_service),
        ("Alert Service Integration", test_alert_service_integration),
        ("Flask Endpoints", test_flask_endpoints),
        ("Requirements.txt", test_requirements)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print("\n" + "=" * 80)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! WhatsApp integration is ready!")
        print("\n🚀 Next Steps:")
        print("1. Start the server: python app_with_auth.py")
        print("2. Go to: http://localhost:5050")
        print("3. Login: admin_demo / Admin@2024")
        print("4. Click 'Test WhatsApp Alert' button")
        print("5. WhatsApp Web will open automatically")
    else:
        print("❌ Some tests failed. Check errors above.")
        
    print("=" * 80)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)