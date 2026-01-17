#!/usr/bin/env python3
"""
Quick Phone Verification Script for Twilio SMS
This script helps verify your phone number with Twilio Trial account
"""

import os
from dotenv import load_dotenv

def verify_phone_number():
    """Verify phone number with Twilio"""
    load_dotenv()
    
    print("📱 Twilio Phone Verification for SMS Alerts")
    print("=" * 50)
    
    # Load Twilio credentials
    twilio_sid = os.getenv('TWILIO_SID')
    twilio_token = os.getenv('TWILIO_TOKEN')
    target_phone = '+917735776771'
    
    if not twilio_sid or not twilio_token:
        print("❌ Twilio credentials not found in .env file")
        return False
    
    print(f"📞 Target Phone: {target_phone}")
    print(f"🔑 Twilio SID: {twilio_sid[:10]}...")
    
    try:
        from twilio.rest import Client
        client = Client(twilio_sid, twilio_token)
        
        print("\n1️⃣ Checking Twilio account status...")
        account = client.api.accounts(twilio_sid).fetch()
        print(f"✅ Account Status: {account.status}")
        print(f"✅ Account Name: {account.friendly_name}")
        
        print("\n2️⃣ Checking if phone number is already verified...")
        
        # List existing outgoing caller IDs (verified numbers)
        try:
            outgoing_caller_ids = client.outgoing_caller_ids.list()
            verified_numbers = [caller_id.phone_number for caller_id in outgoing_caller_ids]
            
            if target_phone in verified_numbers:
                print(f"✅ {target_phone} is already verified!")
                print("🎉 Your SMS should work now. Try the dashboard again.")
                return True
            else:
                print(f"❌ {target_phone} is NOT verified yet.")
                print(f"📋 Currently verified numbers: {verified_numbers}")
        except Exception as e:
            print(f"ℹ️  Could not check verified numbers: {e}")
        
        print("\n3️⃣ Starting phone verification process...")
        print("📝 You have two options:")
        print("   Option A: Manual verification via Twilio Console (RECOMMENDED)")
        print("   Option B: API verification (may not work with trial)")
        
        choice = input("\nChoose option (A/B): ").upper().strip()
        
        if choice == 'A':
            print("\n🌐 MANUAL VERIFICATION STEPS:")
            print("1. Open: https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
            print("2. Click '+ Verify a new number'")
            print(f"3. Enter: {target_phone}")
            print("4. Choose 'Text me' option")
            print("5. Check your phone for verification code")
            print("6. Enter the code in Twilio console")
            print("7. Come back and test SMS in dashboard")
            print("\n✨ This is the most reliable method!")
            
        elif choice == 'B':
            print("\n🚀 Attempting API verification...")
            try:
                validation_request = client.validation_requests.create(
                    phone_number=target_phone,
                    friendly_name="Mining Alert System"
                )
                print(f"✅ Verification request created!")
                print(f"📱 Check your phone {target_phone} for a call or SMS")
                print("🔢 You'll receive a verification code")
                
                # Wait for user to enter verification code
                code = input("\n🔢 Enter the verification code you received: ").strip()
                
                if code:
                    print("📞 Code entered. Verification should be complete.")
                    print("🧪 Test SMS again in your dashboard!")
                else:
                    print("❌ No code entered. Try manual verification instead.")
                    
            except Exception as e:
                print(f"❌ API verification failed: {e}")
                print("💡 Try the manual verification method instead (Option A)")
        else:
            print("❌ Invalid choice. Try again.")
            
    except ImportError:
        print("❌ Twilio library not installed. Run: pip install twilio")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("📋 NEXT STEPS:")
    print("1. Complete phone verification (if not done)")
    print("2. Go to: http://localhost:5050")
    print("3. Login: admin_demo / Admin@2024")
    print("4. Click 'Direct SMS Test' button")
    print("5. You should receive SMS on your phone!")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    verify_phone_number()