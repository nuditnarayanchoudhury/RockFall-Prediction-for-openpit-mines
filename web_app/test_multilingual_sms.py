#!/usr/bin/env python3
"""
Test script for area-based multilingual SMS alert functionality
Tests the new language-specific SMS generation for different Indian mining regions
"""

from datetime import datetime
from alert_service import AlertService

def test_multilingual_sms_alerts():
    """Test SMS generation for different Indian states and their local languages"""
    
    # Initialize alert service
    alert_service = AlertService()
    
    # Test cases for different mining regions
    test_cases = [
        {
            'name': 'West Bengal Coal Mine',
            'location': 'Dhanbad, West Bengal',
            'expected_languages': ['bengali', 'hindi', 'english']
        },
        {
            'name': 'Odisha Iron Ore Mine',
            'location': 'Keonjhar, Odisha',
            'expected_languages': ['odia', 'hindi', 'english']
        },
        {
            'name': 'Karnataka Gold Mine',
            'location': 'Bellary, Karnataka',
            'expected_languages': ['kannada', 'hindi', 'english']
        },
        {
            'name': 'Telangana Coal Mine',
            'location': 'Warangal, Telangana',
            'expected_languages': ['telugu', 'hindi', 'english']
        },
        {
            'name': 'Gujarat Salt Mine',
            'location': 'Kutch, Gujarat',
            'expected_languages': ['gujarati', 'hindi', 'english']
        },
        {
            'name': 'Maharashtra Iron Mine',
            'location': 'Pune, Maharashtra',
            'expected_languages': ['marathi', 'hindi', 'english']
        },
        {
            'name': 'Jharkhand Coal Mine',
            'location': 'Ranchi, Jharkhand',
            'expected_languages': ['hindi', 'english']
        },
        {
            'name': 'Unknown Location Mine',
            'location': 'Some Remote Area',
            'expected_languages': ['hindi', 'english']  # Default fallback
        }
    ]
    
    risk_levels = ['HIGH', 'MEDIUM', 'LOW']
    
    print("=" * 80)
    print("TESTING AREA-BASED MULTILINGUAL SMS ALERTS")
    print("=" * 80)
    
    for test_case in test_cases:
        print(f"\n{'='*60}")
        print(f"TESTING: {test_case['name']}")
        print(f"Location: {test_case['location']}")
        print(f"Expected Languages: {', '.join(test_case['expected_languages']).title()}")
        print(f"{'='*60}")
        
        for risk_level in risk_levels:
            # Create test alert
            test_alert = {
                'id': f'test_{risk_level.lower()}',
                'mine_name': test_case['name'],
                'location': test_case['location'],
                'alert_level': risk_level,
                'risk_score': {'HIGH': 8.7, 'MEDIUM': 5.2, 'LOW': 2.1}[risk_level],
                'timestamp': datetime.now().isoformat(),
                'status': 'ACTIVE'
            }
            
            # Test state extraction
            state = alert_service.extract_state_from_location(test_case['location'])
            languages = alert_service.get_area_languages(state)
            
            print(f"\n--- {risk_level} RISK ALERT ---")
            print(f"Extracted State: {state}")
            print(f"Selected Languages: {', '.join(languages).title()}")
            
            # Generate multilingual SMS
            sms_body = alert_service.generate_sms_body(test_alert)
            
            print(f"\nGenerated SMS:\n{'-'*40}")
            print(sms_body)
            print(f"{'-'*40}")
            
            # Verify language selection matches expected
            if languages == test_case['expected_languages']:
                print("✅ Language selection: CORRECT")
            else:
                print(f"❌ Language selection: INCORRECT")
                print(f"   Expected: {test_case['expected_languages']}")
                print(f"   Got: {languages}")
            
            print("\n" + "."*50)

    print(f"\n{'='*80}")
    print("MULTILINGUAL SMS TESTING COMPLETED")
    print("=" * 80)
    
    # Test individual language components
    print(f"\n{'='*60}")
    print("TESTING LANGUAGE COMPONENTS")
    print(f"{'='*60}")
    
    # Test state extraction
    location_tests = [
        ('Ranchi, Jharkhand', 'JHARKHAND'),
        ('Bhubaneswar, Odisha', 'ODISHA'),
        ('Kolkata, West Bengal', 'WEST_BENGAL'),
        ('Gandhinagar, Gujarat', 'GUJARAT'),
        ('Bengaluru, Karnataka', 'KARNATAKA'),
        ('Hyderabad, Telangana', 'TELANGANA'),
        ('Some Unknown Place', 'DEFAULT')
    ]
    
    print("\nState Extraction Tests:")
    print("-" * 30)
    for location, expected_state in location_tests:
        extracted = alert_service.extract_state_from_location(location)
        status = "✅" if extracted == expected_state else "❌"
        print(f"{status} '{location}' -> {extracted} (expected: {expected_state})")
    
    # Test language mappings
    print("\nLanguage Mapping Tests:")
    print("-" * 30)
    state_lang_tests = [
        ('ODISHA', ['odia', 'hindi', 'english']),
        ('WEST_BENGAL', ['bengali', 'hindi', 'english']),
        ('KARNATAKA', ['kannada', 'hindi', 'english']),
        ('JHARKHAND', ['hindi', 'english']),
        ('DEFAULT', ['hindi', 'english'])
    ]
    
    for state, expected_langs in state_lang_tests:
        actual_langs = alert_service.get_area_languages(state)
        status = "✅" if actual_langs == expected_langs else "❌"
        print(f"{status} {state} -> {actual_langs}")
    
    print(f"\n{'='*80}")
    print("ALL TESTS COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    test_multilingual_sms_alerts()
