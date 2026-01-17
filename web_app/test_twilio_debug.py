#!/usr/bin/env python3
"""
Debug Twilio SMS configuration for high alerts
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_twilio_credentials():
    """Test Twilio credentials and configuration"""
    print("🔍 TWILIO CONFIGURATION DEBUG")
    print("=" * 50)
    
    # Check if credentials are loaded
    twilio_sid = os.getenv('TWILIO_SID')
    twilio_token = os.getenv('TWILIO_TOKEN') 
    twilio_phone = os.getenv('TWILIO_PHONE')
    
    print(f"📱 Twilio SID: {twilio_sid}")
    print(f"🔑 Token configured: {'Yes' if twilio_token else 'No'}")
    print(f"📞 Twilio Phone: {twilio_phone}")
    
    if not all([twilio_sid, twilio_token, twilio_phone]):
        print("\n❌ MISSING CREDENTIALS!")
        print("Make sure all three Twilio credentials are in .env file:")
        print("- TWILIO_SID")
        print("- TWILIO_TOKEN") 
        print("- TWILIO_PHONE")
        return False
    
    # Test Twilio installation
    try:
        from twilio.rest import Client
        print("✅ Twilio library installed")
    except ImportError:
        print("❌ Twilio library not installed")
        print("💡 Run: pip install twilio")
        return False
    
    # Test account connection
    try:
        client = Client(twilio_sid, twilio_token)
        account = client.api.accounts(twilio_sid).fetch()
        print(f"✅ Account connected: {account.friendly_name}")
        print(f"   Status: {account.status}")
        return True
    except Exception as e:
        print(f"❌ Account connection failed: {e}")
        return False

def test_sms_send():
    """Test sending a sample SMS"""
    print("\n🚀 TESTING SMS SEND")
    print("=" * 50)
    
    try:
        from twilio.rest import Client
    except ImportError:
        print("❌ Twilio not installed. Run: pip install twilio")
        return
    
    account_sid = os.getenv('TWILIO_SID')
    auth_token = os.getenv('TWILIO_TOKEN')
    twilio_phone = os.getenv('TWILIO_PHONE')
    
    if not all([account_sid, auth_token, twilio_phone]):
        print("❌ Missing Twilio credentials")
        return
    
    # Use first phone number from emergency list
    test_phones = os.getenv('EMERGENCY_PHONES', '').split(',')
    if not test_phones or not test_phones[0].strip():
        print("❌ No phone numbers configured in EMERGENCY_PHONES")
        return
    
    test_phone = test_phones[0].strip()
    print(f"📱 Testing SMS to: {test_phone}")
    print(f"   From Phone: {twilio_phone}")
    
    try:
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            body="🚨 TEST: AI Rockfall System Alert Test - This is a test message from your mining safety system.",
            from_=twilio_phone,
            to=test_phone
        )
        
        print(f"✅ SMS sent successfully!")
        print(f"   Message SID: {message.sid}")
        print(f"   Status: {message.status}")
        
    except Exception as e:
        print(f"❌ SMS send failed: {e}")
        
        # Common error checks
        error_str = str(e).lower()
        if 'unverified' in error_str:
            print("💡 Your phone number might not be verified with Twilio")
            print("   Go to Twilio Console > Phone Numbers > Manage > Verified Caller IDs")
        elif 'balance' in error_str or 'funds' in error_str:
            print("💡 Check your Twilio account balance")
        elif 'invalid' in error_str and 'phone' in error_str:
            print("💡 Check if phone numbers are in correct international format (+country_code)")

def debug_high_alert_flow():
    """Debug high alert sending flow"""
    print("\n🔥 HIGH ALERT FLOW DEBUG")
    print("=" * 50)
    
    # Check alert service import
    try:
        from alert_service import AlertService
        print("✅ AlertService imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import AlertService: {e}")
        return
    
    # Create alert service
    alert_service = AlertService()
    
    # Check SMS configuration in alert service
    print(f"📱 Alert Service SMS Config:")
    print(f"   SID: {alert_service.twilio_sid}")
    print(f"   Token: {'***' if alert_service.twilio_token else 'None'}")
    print(f"   Phone: {alert_service.twilio_phone}")
    
    # Check phone numbers configuration
    emergency_phones = alert_service.alert_recipients.get('emergency', {}).get('phones', [])
    print(f"📞 Emergency phones configured: {len(emergency_phones)}")
    for i, phone in enumerate(emergency_phones):
        print(f"   {i+1}. {phone}")
    
    # Test sending HIGH alert SMS
    if emergency_phones:
        print(f"\n🧪 Testing HIGH alert SMS sending...")
        
        # Create a mock alert
        mock_alert = {
            'id': 'test_alert_123',
            'mine_id': 'test_mine',
            'mine_name': 'Test Mine',
            'location': 'Test Location, Jharkhand',
            'alert_level': 'HIGH',
            'timestamp': '2024-01-01T12:00:00',
            'risk_score': 0.85,
            'sensor_data': {
                'vibration': 15.2,
                'temperature': 45.3,
                'humidity': 75.1
            }
        }
        
        # Test SMS generation
        sms_body = alert_service.generate_sms_body(mock_alert)
        print(f"📝 Generated SMS (length: {len(sms_body)}):")
        print("-" * 40)
        print(sms_body)
        print("-" * 40)
        
        # Test actual sending
        print("\n🚀 Attempting to send test HIGH alert SMS...")
        sms_result = alert_service.send_sms_alert(mock_alert, ['emergency'])
        
        if sms_result['success']:
            print(f"✅ SMS sent successfully to {sms_result.get('recipients', 0)} recipients")
        else:
            print(f"❌ SMS sending failed: {sms_result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    print("🔧 TWILIO SMS DEBUG FOR HIGH ALERTS")
    print("=" * 60)
    print()
    
    # Step 1: Test credentials
    creds_ok = test_twilio_credentials()
    
    if creds_ok:
        # Step 2: Test basic SMS
        test_sms_send()
        
        # Step 3: Debug high alert flow
        debug_high_alert_flow()
    else:
        print("\n❌ Fix Twilio credentials first before proceeding")
    
    print("\n" + "=" * 60)
    print("📚 For Twilio setup help, see: TWILIO_SETUP_GUIDE.md")