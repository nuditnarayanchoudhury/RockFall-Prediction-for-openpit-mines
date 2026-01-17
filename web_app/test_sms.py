#!/usr/bin/env python3
"""
Test SMS functionality for AI Rockfall Prediction System
This script tests if your Twilio SMS configuration is working
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_sms_configuration():
    """Test SMS configuration and send a test message"""
    
    print("📱 Testing Twilio SMS Configuration...")
    print("=" * 50)
    
    # Check if Twilio is installed
    try:
        from twilio.rest import Client
        print("✅ Twilio library installed")
    except ImportError:
        print("❌ Twilio not installed. Run: pip install twilio")
        return
    
    # Get credentials from environment
    account_sid = os.getenv('TWILIO_SID')
    auth_token = os.getenv('TWILIO_TOKEN')
    twilio_phone = os.getenv('TWILIO_PHONE')
    your_phone = '+917735776771'  # Your phone number
    
    # Check if credentials are configured
    if not account_sid or not auth_token or not twilio_phone:
        print("❌ Twilio credentials not configured in .env file")
        print("\nPlease add to .env:")
        print("TWILIO_SID=your_account_sid_here")
        print("TWILIO_TOKEN=your_auth_token_here") 
        print("TWILIO_PHONE=your_twilio_phone_here")
        return
    
    if account_sid == 'your_twilio_account_sid_here':
        print("❌ Please replace placeholder values with real Twilio credentials")
        return
    
    print(f"📋 Configuration Check:")
    print(f"   Account SID: {account_sid[:8]}...")
    print(f"   Auth Token: {auth_token[:8]}...")
    print(f"   From Phone: {twilio_phone}")
    print(f"   To Phone: {your_phone}")
    print()
    
    # Test SMS sending
    try:
        print("📤 Sending test SMS...")
        
        client = Client(account_sid, auth_token)
        
        # Create bilingual test message
        message_body = """🚨 टेस्ट अलर्ट | TEST ALERT - AI Rockfall System

आपका SMS अलर्ट सिस्टम काम कर रहा है! | Your SMS alert system is working!

यह पुष्टि करता है कि खानों में खतरनाक स्थिति मिलने पर स्वचालित HIGH जोखिम अलर्ट आपके फोन पर भेजे जाएंगे | This confirms that HIGH risk alerts will be automatically sent to your phone when dangerous conditions are detected at mining sites.

- AI शिलाखंड भविष्यवाणी सिस्टम | AI Rockfall Prediction System"""
        
        message = client.messages.create(
            body=message_body,
            from_=twilio_phone,
            to=your_phone
        )
        
        print("✅ SMS sent successfully!")
        print(f"📧 Message SID: {message.sid}")
        print(f"📱 Status: {message.status}")
        print()
        print("🔔 Check your phone for the test message!")
        print("   If you received it, SMS alerts are working perfectly.")
        
        return True
        
    except Exception as e:
        print(f"❌ SMS sending failed: {e}")
        print()
        print("💡 Common solutions:")
        print("   1. Check Account SID and Auth Token are correct")
        print("   2. Verify your Twilio phone number is correct")
        print("   3. Ensure your phone (+917735776771) is verified in Twilio Console")
        print("   4. Check if you have trial credits remaining")
        
        return False

def main():
    """Main test function"""
    print("🚨 AI Rockfall Prediction System - SMS Test")
    print("=" * 50)
    print()
    
    success = test_sms_configuration()
    
    print()
    print("=" * 50)
    if success:
        print("🎉 SMS CONFIGURATION SUCCESSFUL!")
        print("Your automatic alert system is ready to send SMS alerts.")
        print()
        print("Next steps:")
        print("1. Run: python app_with_auth.py")
        print("2. System will automatically send SMS for HIGH risk alerts")
        print("3. You'll receive both EMAIL and SMS notifications")
    else:
        print("🔧 SMS CONFIGURATION NEEDS ATTENTION")
        print("Please fix the issues above and try again.")
    print("=" * 50)

if __name__ == '__main__':
    main()
