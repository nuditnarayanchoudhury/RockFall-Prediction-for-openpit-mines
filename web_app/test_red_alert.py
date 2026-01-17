#!/usr/bin/env python3
"""
Test script to trigger red alerts for demonstration
This script sends a test request to generate high-risk alerts
"""

import requests
import json
import time

def trigger_test_alert():
    """Send test alert to demonstrate red alert banner"""
    try:
        response = requests.post(
            'http://localhost:5000/api/send_test_alert',
            headers={'Content-Type': 'application/json'},
            json={
                'mine_id': 'mine_001',
                'type': 'high_risk_test'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Test alert sent successfully!")
            print(f"📊 Response: {result.get('message', 'Alert triggered')}")
            return True
        else:
            print(f"❌ Failed to send test alert. Status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending test alert: {e}")
        return False

def check_predictions():
    """Check current predictions to see if any mines are high risk"""
    try:
        response = requests.get('http://localhost:5000/api/predictions', timeout=10)
        
        if response.status_code == 200:
            predictions = response.json()
            high_risk_mines = [p for p in predictions if p.get('risk_level') == 'HIGH']
            
            print(f"🏔️  Total mines monitored: {len(predictions)}")
            print(f"🚨 High risk mines: {len(high_risk_mines)}")
            
            if high_risk_mines:
                print("\n⚠️  HIGH RISK MINES DETECTED:")
                for mine in high_risk_mines:
                    print(f"   • {mine['mine_name']} ({mine['location']})")
                    print(f"     Risk Score: {mine.get('risk_score', 'N/A'):.3f}")
                    print(f"     Confidence: {mine.get('confidence', 'N/A'):.3f}")
                print(f"\n🔔 Red alert banner should be visible on dashboard!")
            else:
                print("\n✅ No high risk mines currently detected")
                
            return high_risk_mines
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error checking predictions: {e}")
        return []

def main():
    print("=" * 60)
    print("🏔️  Red Alert Banner Test System")
    print("=" * 60)
    
    print("\n1️⃣  Checking current mine status...")
    high_risk_mines = check_predictions()
    
    if not high_risk_mines:
        print("\n2️⃣  No high risk alerts found. Triggering test alert...")
        if trigger_test_alert():
            print("\n⏳ Waiting 3 seconds for system to update...")
            time.sleep(3)
            
            print("\n3️⃣  Checking updated mine status...")
            high_risk_mines = check_predictions()
    
    print(f"\n🎯 RESULT:")
    if high_risk_mines:
        print(f"✅ SUCCESS! {len(high_risk_mines)} high risk mine(s) detected")
        print("🔔 Red alert banner should now be visible on the dashboard")
        print("🌐 Open http://localhost:5000 to see the red alert banner")
        print("\n📋 Features to test:")
        print("   • Red alert banner at top of page")
        print("   • Pulsing animation and alert sound")
        print("   • 'View Details' button navigates to Alerts tab")
        print("   • 'X' button dismisses alert (stays dismissed for 10 minutes)")
        print("   • Alert reappears on page refresh if still high risk")
    else:
        print("❌ No high risk alerts generated. Try running the dashboard first.")
    
    print(f"\n" + "=" * 60)

if __name__ == "__main__":
    main()
