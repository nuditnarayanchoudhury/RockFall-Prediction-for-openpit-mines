#!/usr/bin/env python3
"""
Test script for SMS functionality from dashboard
This tests all three SMS endpoints to ensure they work correctly
"""

import requests
import json
from datetime import datetime

def test_dashboard_sms():
    """Test SMS functionality through Flask endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Dashboard SMS Functionality")
    print("=" * 60)
    
    # Test credentials (using demo admin account)
    login_data = {
        'username': 'admin_demo',
        'password': 'Admin@2024'
    }
    
    session = requests.Session()
    
    # Step 1: Login
    print("\n1️⃣ Testing Login...")
    try:
        login_response = session.post(f"{base_url}/login", data=login_data)
        if login_response.status_code == 200 and "dashboard" in login_response.text.lower():
            print("✅ Login successful")
        else:
            print("❌ Login failed")
            return False
    except requests.ConnectionError:
        print("❌ Cannot connect to Flask app. Make sure it's running with: python app_with_auth.py")
        return False
    
    # Step 2: Test Quick SMS (our new endpoint)
    print("\n2️⃣ Testing Quick SMS (Direct SMS Test Button)...")
    try:
        quick_sms_data = {'mine_id': 'mine_001'}
        response = session.post(f"{base_url}/api/quick_sms_test", 
                               json=quick_sms_data,
                               headers={'Content-Type': 'application/json'})
        
        result = response.json()
        if result.get('success'):
            print(f"✅ Quick SMS test successful!")
            print(f"   Message: {result.get('message', 'No message')}")
            print(f"   Mine: {result.get('mine_name', 'Unknown')}")
        else:
            print(f"❌ Quick SMS test failed: {result.get('error', 'Unknown error')}")
            print(f"   Details: {result}")
            
    except Exception as e:
        print(f"❌ Quick SMS test error: {e}")
    
    # Step 3: Test Alert SMS (dashboard button functionality)
    print("\n3️⃣ Testing Alert SMS (Dashboard SMS Alert Button)...")
    try:
        alert_sms_data = {
            'mine_id': 'mine_001',
            'alert_id': 'test_alert_001'
        }
        response = session.post(f"{base_url}/api/send_alert_sms", 
                               json=alert_sms_data,
                               headers={'Content-Type': 'application/json'})
        
        result = response.json()
        if result.get('success'):
            print(f"✅ Alert SMS test successful!")
            print(f"   Message: {result.get('message', 'No message')}")
            alert_details = result.get('alert_details', {})
            print(f"   Mine: {alert_details.get('mine_name', 'Unknown')}")
            print(f"   Risk Level: {alert_details.get('risk_level', 'Unknown')}")
            print(f"   Risk Score: {alert_details.get('risk_score', 'Unknown')}")
            print(f"   Recipients: {alert_details.get('recipients', 0)}")
        else:
            print(f"❌ Alert SMS test failed: {result.get('error', 'Unknown error')}")
            print(f"   Details: {result.get('details', 'No details')}")
            
    except Exception as e:
        print(f"❌ Alert SMS test error: {e}")
    
    # Step 4: Test SMS with phone number (original test function)
    print("\n4️⃣ Testing SMS with Custom Phone (Test SMS Alert Button)...")
    try:
        test_sms_data = {
            'mine_id': 'mine_001',
            'phone': '+917735776771'
        }
        response = session.post(f"{base_url}/api/test_sms", 
                               json=test_sms_data,
                               headers={'Content-Type': 'application/json'})
        
        result = response.json()
        if result.get('success'):
            print(f"✅ Custom SMS test successful!")
            print(f"   Sent to: {result.get('to', 'Unknown')}")
            if 'xai_enabled' in result:
                print(f"   XAI Enabled: {result['xai_enabled']}")
        else:
            print(f"❌ Custom SMS test failed: {result.get('error', 'Unknown error')}")
            if 'solution' in result:
                print(f"   Solution: {result['solution']}")
            
    except Exception as e:
        print(f"❌ Custom SMS test error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Test Summary:")
    print("   ✅ = SMS functionality working correctly")
    print("   ❌ = Issue detected (check error messages above)")
    print("\n📱 If you received SMS messages, the dashboard buttons should work!")
    print("\n🚀 Now test the dashboard:")
    print("   1. Open: http://localhost:5000")
    print("   2. Login with: admin_demo / Admin@2024")
    print("   3. Click 'Direct SMS Test' button in Active Alerts section")
    print("   4. Click 'Send SMS Alert' on any high-risk mine")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    test_dashboard_sms()