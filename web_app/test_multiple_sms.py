#!/usr/bin/env python3
"""
Test SMS functionality for multiple phone numbers
AI Rockfall Prediction System - Multi-recipient SMS Test
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_multiple_sms():
    """Test SMS to multiple phone numbers"""
    
    print("📱 Testing SMS for Multiple Recipients")
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
    
    # Get all phone numbers
    emergency_phones = os.getenv('EMERGENCY_PHONES', '').split(',')
    phone_numbers = [phone.strip() for phone in emergency_phones if phone.strip()]
    
    if not account_sid or not auth_token or not twilio_phone:
        print("❌ Twilio credentials not configured")
        return
    
    if not phone_numbers:
        print("❌ No phone numbers configured")
        return
    
    print(f"📋 Configuration:")
    print(f"   Account SID: {account_sid[:8]}...")
    print(f"   From Phone: {twilio_phone}")
    print(f"   Recipients: {len(phone_numbers)} numbers")
    for i, phone in enumerate(phone_numbers, 1):
        print(f"     {i}. {phone}")
    print()
    
    try:
        client = Client(account_sid, auth_token)
        
        # Create test message
        message_body = """🚨 MULTI-RECIPIENT TEST - AI Rockfall System

This is a test to verify that HIGH risk alerts will be sent to multiple team members when dangerous mining conditions are detected.

Recipients:
• 7735776771
• 7815015581  
• 9078280686

- AI Rockfall Prediction System"""
        
        success_count = 0
        total_numbers = len(phone_numbers)
        
        print("📤 Sending SMS to all recipients...")
        print()
        
        for i, phone_number in enumerate(phone_numbers, 1):
            try:
                print(f"   {i}/{total_numbers} Sending to {phone_number}... ", end="")
                
                message = client.messages.create(
                    body=message_body,
                    from_=twilio_phone,
                    to=phone_number
                )
                
                print(f"✅ SUCCESS (ID: {message.sid[:10]}...)")
                success_count += 1
                
            except Exception as e:
                print(f"❌ FAILED: {e}")
        
        print()
        print("=" * 50)
        print(f"📊 RESULTS SUMMARY:")
        print(f"   Total Recipients: {total_numbers}")
        print(f"   Successful Sends: {success_count}")
        print(f"   Failed Sends: {total_numbers - success_count}")
        print(f"   Success Rate: {(success_count/total_numbers)*100:.1f}%")
        
        if success_count == total_numbers:
            print()
            print("🎉 ALL SMS SENT SUCCESSFULLY!")
            print("📱 All team members should receive the test message")
            print("✅ Your multi-recipient alert system is ready!")
        elif success_count > 0:
            print()
            print("⚠️  PARTIAL SUCCESS")
            print("Some messages sent, others failed. Check error messages above.")
        else:
            print()
            print("❌ ALL SENDS FAILED")
            print("Check your Twilio configuration and phone number formats.")
        
        return success_count == total_numbers
        
    except Exception as e:
        print(f"❌ SMS system error: {e}")
        return False

def main():
    """Main test function"""
    print("🚨 AI Rockfall System - Multi-Recipient SMS Test")
    print("=" * 50)
    print()
    
    success = test_multiple_sms()
    
    print()
    print("=" * 50)
    if success:
        print("🎉 MULTI-RECIPIENT SMS SYSTEM READY!")
        print()
        print("Your automatic alert system will now send SMS to:")
        print("📱 7735776771 (Primary)")
        print("📱 7815015581 (Secondary)")
        print("📱 9078280686 (Tertiary)")
        print()
        print("When HIGH risk is detected, ALL THREE numbers will")
        print("receive immediate SMS notifications!")
    else:
        print("🔧 CONFIGURATION NEEDS ATTENTION")
        print("Some recipients may not receive alerts.")
        print("Check the error messages above.")
    print("=" * 50)

if __name__ == '__main__':
    main()
