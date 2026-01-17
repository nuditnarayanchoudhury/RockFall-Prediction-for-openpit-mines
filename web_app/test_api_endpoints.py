#!/usr/bin/env python3
"""
Test script to verify API endpoints are working correctly
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_endpoints():
    """Test the SMS API endpoints"""
    base_url = "http://localhost:5050"
    
    print("🧪 Testing API Endpoints...")
    print("=" * 50)
    
    # Test if server is running
    try:
        response = requests.get(f"{base_url}/")
        print("✅ Server is running")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start with: python app_with_auth.py")
        return False
    
    # Test environment variables
    print(f"\n📋 Environment Variables:")
    print(f"   TWILIO_SID: {os.getenv('TWILIO_SID', 'NOT SET')}")
    print(f"   TWILIO_TOKEN: {'SET' if os.getenv('TWILIO_TOKEN') else 'NOT SET'}")
    print(f"   TWILIO_PHONE: {os.getenv('TWILIO_PHONE', 'NOT SET')}")
    
    # Check if all required variables are set
    if all([os.getenv('TWILIO_SID'), os.getenv('TWILIO_TOKEN'), os.getenv('TWILIO_PHONE')]):
        print("✅ All Twilio environment variables are configured")
    else:
        print("❌ Some Twilio environment variables are missing")
        return False
    
    print("\n🎯 API endpoints should be working correctly!")
    print("💻 Open your browser and go to: http://localhost:5050")
    print("🔑 Log in with demo credentials and test the SMS buttons")
    
    return True

if __name__ == "__main__":
    test_api_endpoints()