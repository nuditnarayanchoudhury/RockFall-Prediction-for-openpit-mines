#!/usr/bin/env python3
"""
Test script for SMS functionality with updated Twilio credentials
"""

import os
from dotenv import load_dotenv
from twilio.rest import Client
from datetime import datetime

def load_config():
    """Load configuration from .env file"""
    load_dotenv()
    return {
        'twilio_sid': os.getenv('TWILIO_SID'),
        'twilio_token': os.getenv('TWILIO_TOKEN'),
        'twilio_phone': os.getenv('TWILIO_PHONE'),
        'verified_phone': os.getenv('VERIFIED_PHONE', '+917735776771'),
        'secondary_phone': '+919078280686'
    }

def test_twilio_connection(config):
    """Test Twilio connection and account info"""
    print("🔗 Testing Twilio Connection...")
    try:
        client = Client(config['twilio_sid'], config['twilio_token'])
        account = client.api.account.fetch()
        print(f"✅ Connected to Twilio Account: {account.friendly_name}")
        print(f"   Account SID: {account.sid}")
        print(f"   Status: {account.status}")
        return client
    except Exception as e:
        print(f"❌ Twilio connection failed: {e}")
        return None

def test_direct_sms(client, config):
    """Test direct SMS to verified number"""
    print(f"\n📱 Testing Direct SMS to {config['verified_phone']}...")
    
    try:
        message = client.messages.create(
            body="Test SMS from Updated Disaster Management System - Connection successful!",
            from_=config['twilio_phone'],
            to=config['verified_phone']
        )
        
        print(f"✅ SMS sent successfully!")
        print(f"   Message SID: {message.sid}")
        print(f"   Status: {message.status}")
        print(f"   From: {config['twilio_phone']}")
        print(f"   To: {config['verified_phone']}")
        
        return True
        
    except Exception as e:
        print(f"❌ SMS failed: {e}")
        return False

def test_both_numbers(client, config):
    """Test SMS to both verified numbers"""
    print(f"\n📱📱 Testing SMS to both verified numbers...")
    
    test_numbers = [config['verified_phone'], config['secondary_phone']]
    results = []
    
    for i, phone_number in enumerate(test_numbers, 1):
        print(f"\n   Test {i}: Sending to {phone_number}...")
        
        try:
            message = client.messages.create(
                body=f"Multi-number SMS test {i}/2 from Disaster Management System - All systems operational. Time: {datetime.now().strftime('%H:%M:%S')}",
                from_=config['twilio_phone'],
                to=phone_number
            )
            
            results.append({
                'phone': phone_number,
                'success': True,
                'sid': message.sid,
                'status': message.status
            })
            
            print(f"   ✅ Success! SID: {message.sid}, Status: {message.status}")
            
        except Exception as e:
            results.append({
                'phone': phone_number,
                'success': False,
                'error': str(e)
            })
            print(f"   ❌ Failed: {e}")
    
    # Summary
    successful = sum(1 for r in results if r['success'])
    print(f"\n📊 Multi-number test summary: {successful}/{len(results)} successful")
    
    return results

def test_alert_style_sms(client, config):
    """Test SMS with alert-style formatting"""
    print(f"\n🚨 Testing Alert-Style SMS...")
    
    alert_message = """🚨 ROCKFALL ALERT | शिलाखंड अलर्ट

Mine | खान: Jharia Coal Mine
Risk | जोखिम: HIGH RISK | अत्यधिक खतरा
Time | समय: {time}
Score | स्कोर: 8.5

EVACUATE NOW! Stop operations! | तुरंत निकासी करें! ऑपरेशन बंद करें!

- AI Rockfall System | AI शिलाखंड सिस्टम""".format(
        time=datetime.now().strftime('%H:%M')
    )
    
    try:
        message = client.messages.create(
            body=alert_message,
            from_=config['twilio_phone'],
            to=config['verified_phone']
        )
        
        print(f"✅ Alert-style SMS sent successfully!")
        print(f"   Message SID: {message.sid}")
        print(f"   Status: {message.status}")
        print(f"   Length: {len(alert_message)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Alert-style SMS failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("🧪 SMS FUNCTIONALITY TEST - UPDATED CREDENTIALS")
    print("=" * 60)
    
    # Load configuration
    config = load_config()
    
    # Verify config
    print("🔧 Configuration Check:")
    print(f"   Twilio SID: {'✅ Set' if config['twilio_sid'] else '❌ Missing'}")
    print(f"   Twilio Token: {'✅ Set' if config['twilio_token'] else '❌ Missing'}")
    print(f"   Twilio Phone: {config['twilio_phone'] or '❌ Missing'}")
    print(f"   Verified Phone: {config['verified_phone']}")
    print(f"   Secondary Phone: {config['secondary_phone']}")
    
    if not all([config['twilio_sid'], config['twilio_token'], config['twilio_phone']]):
        print("\n❌ Missing required Twilio credentials!")
        return
    
    # Test connection
    client = test_twilio_connection(config)
    if not client:
        return
    
    # Test direct SMS
    test_direct_sms(client, config)
    
    # Wait a moment before next test
    import time
    time.sleep(2)
    
    # Test both numbers
    test_both_numbers(client, config)
    
    # Wait a moment before final test
    time.sleep(2)
    
    # Test alert-style SMS
    test_alert_style_sms(client, config)
    
    print("\n" + "=" * 60)
    print("🎉 SMS TESTING COMPLETED")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Check your phones for received messages")
    print("2. If messages didn't arrive, verify phone numbers are correct")
    print("3. Check Twilio console for message status")
    print("4. Test the web dashboard SMS buttons")

if __name__ == "__main__":
    main()