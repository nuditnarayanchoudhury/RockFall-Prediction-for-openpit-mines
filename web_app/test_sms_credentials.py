#!/usr/bin/env python3
"""
Simple script to test Twilio SMS credentials
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_twilio_credentials():
    """Test Twilio SMS credentials"""
    print("🔧 Testing Twilio SMS Credentials")
    print("=" * 50)
    
    # Get credentials
    twilio_sid = os.getenv('TWILIO_SID')
    twilio_token = os.getenv('TWILIO_TOKEN') 
    twilio_phone = os.getenv('TWILIO_PHONE')
    test_phone = '+917735776771'  # Test number
    
    print(f"📱 Twilio SID: {twilio_sid}")
    print(f"🔑 Token configured: {'Yes' if twilio_token else 'No'}")
    print(f"📞 Twilio Phone: {twilio_phone}")
    print(f"🎯 Test Phone: {test_phone}")
    print()
    
    if not all([twilio_sid, twilio_token, twilio_phone]):
        print("❌ ERROR: Missing Twilio credentials in .env file")
        return False
    
    try:
        from twilio.rest import Client
        print("✅ Twilio library imported successfully")
        
        # Test client creation
        client = Client(twilio_sid, twilio_token)
        print("✅ Twilio client created successfully")
        
        # Test account info
        account = client.api.accounts(twilio_sid).fetch()
        print(f"✅ Account status: {account.status}")
        print(f"✅ Account name: {account.friendly_name}")
        
        # Test SMS sending
        print("\n📤 Sending test SMS...")
        message = client.messages.create(
            body="🧪 TEST SMS from AI Rockfall System - Credentials working!",
            from_=twilio_phone,
            to=test_phone
        )
        
        print(f"✅ SMS sent successfully!")
        print(f"📱 Message SID: {message.sid}")
        print(f"📊 Status: {message.status}")
        return True
        
    except ImportError:
        print("❌ ERROR: Twilio library not installed")
        print("💡 Run: pip install twilio")
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        
        if "20003" in str(e):
            print("\n🔍 DIAGNOSIS: Authentication Error (20003)")
            print("📝 Possible solutions:")
            print("   1. Check if Twilio SID and Token are correct")
            print("   2. Verify account is not suspended")
            print("   3. Check if trial account has expired")
            print("   4. Ensure phone numbers are verified for trial accounts")
            
        elif "21211" in str(e):
            print("\n🔍 DIAGNOSIS: Invalid Phone Number")
            print("📝 Check phone number format: +1234567890")
            
        elif "21614" in str(e):
            print("\n🔍 DIAGNOSIS: 'To' number not verified")
            print("📝 For trial accounts, verify the recipient number in Twilio Console")
            
        return False

if __name__ == "__main__":
    success = test_twilio_credentials()
    
    if success:
        print("\n🎉 ALL TESTS PASSED! SMS system is working correctly.")
    else:
        print("\n⚠️  SMS system needs configuration. Check the errors above.")
        print("\n📚 For Twilio setup help, see: TWILIO_SETUP_GUIDE.md")