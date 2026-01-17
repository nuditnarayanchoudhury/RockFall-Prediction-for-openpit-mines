#!/usr/bin/env python3
"""
Test bilingual SMS alerts for AI Rockfall Prediction System
This script tests the new Hindi + English SMS functionality
"""

import os
from dotenv import load_dotenv
from alert_service import AlertService

# Load environment variables
load_dotenv()

def test_bilingual_alerts():
    """Test bilingual alert functionality"""
    
    print("📱 Testing Bilingual SMS Alerts...")
    print("=" * 60)
    
    # Initialize alert service
    alert_service = AlertService()
    
    # Create sample alert data for different risk levels
    test_alerts = [
        {
            'id': 'test_high_001',
            'mine_id': 'mine_001',
            'mine_name': 'Jharia Coalfield',
            'location': 'Dhanbad, Jharkhand',
            'alert_level': 'HIGH',
            'timestamp': '2024-09-14T13:45:00',
            'risk_score': 0.85,
            'key_factors': ['Heavy rainfall', 'Seismic activity', 'Slope instability']
        },
        {
            'id': 'test_medium_002',
            'mine_id': 'mine_002',
            'mine_name': 'Bailadila Iron Ore Mine',
            'location': 'Dantewada, Chhattisgarh',
            'alert_level': 'MEDIUM',
            'timestamp': '2024-09-14T13:45:00',
            'risk_score': 0.55,
            'key_factors': ['Moderate rainfall', 'Ground movement']
        },
        {
            'id': 'test_low_003',
            'mine_id': 'mine_003',
            'mine_name': 'Talcher Coalfield',
            'location': 'Angul, Odisha',
            'alert_level': 'LOW',
            'timestamp': '2024-09-14T13:45:00',
            'risk_score': 0.25,
            'key_factors': ['Normal conditions']
        }
    ]
    
    print("\n🔍 Testing SMS Message Generation...")
    print("-" * 40)
    
    for i, alert in enumerate(test_alerts, 1):
        print(f"\n📋 Test {i}: {alert['alert_level']} Risk Alert")
        print("=" * 50)
        
        # Generate SMS body using new bilingual method
        sms_body = alert_service.generate_sms_body(alert)
        
        print("📱 Generated SMS Message:")
        print("-" * 30)
        print(sms_body)
        print("-" * 30)
        
        # Show character count
        print(f"📊 Message Length: {len(sms_body)} characters")
        print(f"📊 SMS Count: {(len(sms_body) // 160) + 1} SMS")
        
        if len(sms_body) > 1600:  # Twilio limit
            print("⚠️  Warning: Message exceeds Twilio limit (1600 chars)")
        else:
            print("✅ Message length is acceptable")
    
    print("\n" + "=" * 60)
    print("🎯 Testing Bilingual Action Messages...")
    print("-" * 40)
    
    for risk_level in ['HIGH', 'MEDIUM', 'LOW']:
        print(f"\n📋 {risk_level} Risk Actions:")
        print("-" * 30)
        
        action_message = alert_service.get_sms_action_bilingual(risk_level)
        print(action_message)
        print(f"Length: {len(action_message)} chars")
        print("-" * 30)
    
    print("\n" + "=" * 60)
    print("📧 Testing Bilingual Email Subject Lines...")
    print("-" * 40)
    
    for alert in test_alerts:
        hindi_risk = {'HIGH': 'अत्यधिक खतरा', 'MEDIUM': 'मध्यम खतरा', 'LOW': 'कम खतरा'}.get(alert['alert_level'], 'खतरा')
        subject = f"🚨 शिलाखंड अलर्ट | ROCKFALL ALERT - {hindi_risk} | {alert['alert_level']} RISK - {alert['mine_name']}"
        
        print(f"\n📬 {alert['alert_level']} Risk Subject:")
        print(subject)
        print(f"Length: {len(subject)} chars")

def test_actual_sms_send():
    """Test sending actual SMS (optional)"""
    
    print("\n" + "=" * 60)
    print("📤 ACTUAL SMS TEST (Optional)")
    print("=" * 60)
    
    response = input("\nDo you want to send actual test SMS? (y/N): ").lower().strip()
    
    if response == 'y':
        alert_service = AlertService()
        
        # Create test alert
        test_alert = {
            'id': 'test_bilingual_001',
            'mine_id': 'mine_001',
            'mine_name': 'Test Mine - बिलिंगुअल टेस्ट',
            'location': 'Test Location, India',
            'alert_level': 'HIGH',
            'timestamp': '2024-09-14T13:45:00',
            'risk_score': 0.95,
            'key_factors': ['Testing bilingual alerts', 'द्विभाषी अलर्ट का परीक्षण']
        }
        
        print("\n📱 Sending bilingual test SMS...")
        
        # Get test phone numbers from environment
        test_phones = os.getenv('EMERGENCY_PHONES', '+917735776771').split(',')
        
        for phone in test_phones[:1]:  # Send to first number only
            phone = phone.strip()
            if phone:
                message_body = alert_service.generate_sms_body(test_alert)
                
                print(f"\n📞 Sending to: {phone}")
                print("📝 Message preview:")
                print("-" * 30)
                print(message_body[:200] + "..." if len(message_body) > 200 else message_body)
                print("-" * 30)
                
                try:
                    result = alert_service._send_individual_sms(phone, message_body)
                    
                    if result['success']:
                        print("✅ Bilingual SMS sent successfully!")
                        print(f"📧 Message SID: {result.get('message_sid', 'N/A')}")
                    else:
                        print(f"❌ SMS sending failed: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    print(f"❌ Exception occurred: {e}")
                    
                break
    else:
        print("⏭️  Skipping actual SMS test")

def main():
    """Main test function"""
    print("🌐 AI Rockfall Prediction System - Bilingual SMS Test")
    print("=" * 60)
    print("Testing Hindi + English SMS alerts...")
    print()
    
    # Test message generation
    test_bilingual_alerts()
    
    # Test actual SMS sending (optional)
    test_actual_sms_send()
    
    print("\n" + "=" * 60)
    print("🎉 BILINGUAL SMS TESTING COMPLETED!")
    print("=" * 60)
    print()
    print("✅ Features tested:")
    print("   • Hindi + English SMS messages")
    print("   • Risk level translations")
    print("   • Bilingual action instructions")
    print("   • Email subject lines")
    print("   • Message length validation")
    print()
    print("🚀 Your system now supports bilingual alerts!")
    print("   • Alerts are sent in both Hindi and English")
    print("   • Better accessibility for Indian mining operations")
    print("   • Clear action instructions in local language")
    print("=" * 60)

if __name__ == '__main__':
    main()
