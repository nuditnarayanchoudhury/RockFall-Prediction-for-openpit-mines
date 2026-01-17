#!/usr/bin/env python3
"""Test the improved SMS service with better error handling"""

from alert_service import AlertService
from datetime import datetime

def test_improved_sms():
    """Test improved SMS service"""
    print("🔄 Testing Improved SMS Service with Error Handling...")
    print("=" * 60)
    
    # Initialize alert service
    alert_service = AlertService()
    
    # Create test alert
    test_alert = {
        'id': 'improved_test_001',
        'mine_id': 'mine_001',
        'mine_name': 'Jharia Coalfield',
        'location': 'Dhanbad, Jharkhand',
        'alert_level': 'HIGH',
        'timestamp': datetime.now().isoformat(),
        'risk_score': 8.5,
        'sensor_data': {
            'vibration': 8.2,
            'acoustic': 95.0,
            'temperature': 42.0
        }
    }
    
    # Test SMS sending
    result = alert_service.send_sms_alert(test_alert, ['emergency'])
    
    print("📊 SMS Test Results:")
    print(f"  Success: {result.get('success', False)}")
    print(f"  Recipients: {result.get('recipients', 0)}")
    print(f"  Failed: {result.get('failed', 0)}")
    print(f"  Total Attempted: {result.get('total_attempted', 0)}")
    
    if 'error_details' in result:
        print("\n❌ Error Details:")
        for error in result['error_details']:
            print(f"  - {error}")
    
    if 'common_errors' in result:
        print(f"\n🔍 Analysis: {result['common_errors']}")
    
    if 'suggestions' in result:
        print("\n💡 Suggestions:")
        for suggestion in result['suggestions']:
            print(f"  - {suggestion}")
    
    print("\n" + "=" * 60)
    
    if not result.get('success'):
        print("📱 ALTERNATIVE SOLUTION:")
        print("Since SMS is failing due to carrier restrictions, you have options:")
        print("1. ✅ Email alerts are working (check your email)")
        print("2. 📱 Try WhatsApp: python whatsapp_alert.py")
        print("3. 🇮🇳 Use Indian SMS service (MSG91, TextLocal)")
        print("4. 💰 Upgrade Twilio to paid account")
        print("5. 🏗️ Dashboard notifications are working")
    
    return result.get('success', False)

if __name__ == "__main__":
    test_improved_sms()