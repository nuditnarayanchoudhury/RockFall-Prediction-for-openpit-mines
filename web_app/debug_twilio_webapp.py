#!/usr/bin/env python3
"""
Debug script to test Twilio environment variables in the web app context
"""

import os
from dotenv import load_dotenv
from twilio.rest import Client

# Load environment variables (same as in app_with_auth.py)
load_dotenv()

def debug_twilio_in_webapp():
    """Debug Twilio configuration in web app context"""
    print("🔍 Debugging Twilio Configuration for Web App")
    print("=" * 60)
    
    # Check environment variables
    print("\n📋 Environment Variables:")
    twilio_sid = os.getenv('TWILIO_SID')
    twilio_token = os.getenv('TWILIO_TOKEN') 
    twilio_phone = os.getenv('TWILIO_PHONE')
    
    print(f"   TWILIO_SID: {twilio_sid}")
    print(f"   TWILIO_TOKEN: {'SET' if twilio_token else 'NOT SET'}")
    print(f"   TWILIO_PHONE: {twilio_phone}")
    
    # Test if all are configured
    if not all([twilio_sid, twilio_token, twilio_phone]):
        print("\n❌ Missing credentials!")
        print(f"   SID configured: {bool(twilio_sid)}")
        print(f"   Token configured: {bool(twilio_token)}")
        print(f"   Phone configured: {bool(twilio_phone)}")
        return False
    
    # Test Twilio client creation (same as in test_sms endpoint)
    print("\n🧪 Testing Twilio Client Creation...")
    try:
        client = Client(twilio_sid, twilio_token)
        print("✅ Twilio client created successfully")
        
        # Test account fetch (like the web app does)
        try:
            account = client.api.accounts(twilio_sid).fetch()
            print(f"✅ Account verified: {account.friendly_name}")
            print(f"✅ Account status: {account.status}")
            
            # Test SMS sending (minimal test)
            print("\n📤 Testing SMS sending...")
            message = client.messages.create(
                body="🧪 DEBUG: Twilio test from web app context - credentials working!",
                from_=twilio_phone,
                to='+917735776771'  # Your verified number
            )
            print(f"✅ SMS sent successfully!")
            print(f"   Message SID: {message.sid}")
            print(f"   Status: {message.status}")
            
            return True
            
        except Exception as account_error:
            print(f"❌ Account verification failed: {account_error}")
            if "20003" in str(account_error):
                print("🔍 This is the same 20003 error you're seeing in the web app!")
            return False
            
    except Exception as client_error:
        print(f"❌ Twilio client creation failed: {client_error}")
        return False

if __name__ == "__main__":
    debug_twilio_in_webapp()