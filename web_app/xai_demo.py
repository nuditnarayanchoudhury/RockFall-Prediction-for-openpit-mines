#!/usr/bin/env python3
"""
XAI Risk Explanation Demo

This demo shows how the new Explainable AI functionality works in the rockfall alert system.
It demonstrates what mine operators will see when high-risk alerts are triggered.
"""

import json
from datetime import datetime
from alert_service import AlertService
from risk_explainer import RockfallRiskExplainer

def create_demo_high_risk_scenario():
    """Create a realistic high-risk scenario for demonstration"""
    return {
        'mine_id': 'demo_mine_001',
        'mine_name': 'Jharkhand Coal Complex - Block A',
        'location': 'Dhanbad District, Jharkhand',
        'alert_level': 'HIGH',
        'risk_score': 8.7,
        'sensor_data': {
            'vibration': 8.2,         # CRITICAL - well above 7.5 threshold
            'temperature': 43.1,      # HIGH - above 40°C threshold  
            'humidity': 89.3,         # HIGH - above 85% threshold
            'pressure': 1018.5,       # LOW - within normal range
            'acoustic': 96.4,         # CRITICAL - above 100dB threshold
            'slope_stability': 0.41   # HIGH - above 0.3 threshold
        },
        'historical_data': [
            {'vibration': 3.2, 'temperature': 28.1, 'humidity': 62.3, 'acoustic': 52.1},
            {'vibration': 4.1, 'temperature': 31.5, 'humidity': 68.7, 'acoustic': 58.9},
            {'vibration': 5.8, 'temperature': 35.2, 'humidity': 74.2, 'acoustic': 71.3},
            {'vibration': 6.9, 'temperature': 38.8, 'humidity': 81.1, 'acoustic': 84.7},
            {'vibration': 7.5, 'temperature': 41.2, 'humidity': 86.5, 'acoustic': 91.2}
        ],
        'context': {
            'shift': 'Morning Shift - 06:00 to 14:00',
            'workers_present': 23,
            'active_equipment': ['Excavator-01', 'Loader-03', 'Drill-02'],
            'weather_conditions': 'Heavy monsoon rains in past 48 hours'
        }
    }

def demonstrate_before_vs_after():
    """Show the difference between old alerts and new XAI-enhanced alerts"""
    
    scenario = create_demo_high_risk_scenario()
    alert_service = AlertService()
    
    print("🔄 ROCKFALL ALERT SYSTEM - BEFORE vs AFTER XAI")
    print("=" * 80)
    
    # === BEFORE XAI (OLD SYSTEM) ===
    print("\n📱 BEFORE XAI - Traditional Alert (What operators used to see):")
    print("=" * 60)
    
    old_style_sms = f"""🚨 शिलाखंड अलर्ट | ROCKFALL ALERT

खान | Mine: {scenario['mine_name']}
जोखिम | Risk: अत्यधिक खतरा | HIGH RISK
समय | Time: {datetime.now().strftime('%H:%M')}
स्कोर | Score: {scenario['risk_score']}

तुरंत निकासी करें! ऑपरेशन बंद करें! | EVACUATE NOW! Stop operations!

- AI शिलाखंड सिस्टम | AI Rockfall System"""

    print("SMS Alert:")
    print("-" * 30)
    print(old_style_sms)
    print("-" * 30)
    print("❌ PROBLEM: No explanation of WHY there's high risk!")
    print("❌ PROBLEM: Operators don't know which sensors are critical!")
    print("❌ PROBLEM: No specific guidance on what to check!")
    
    # === AFTER XAI (NEW SYSTEM) ===
    print(f"\n📱 AFTER XAI - Explainable Alert (What operators see now):")
    print("=" * 60)
    
    # Create full alert with XAI explanation
    alert = {
        'id': f"demo_alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'mine_id': scenario['mine_id'],
        'mine_name': scenario['mine_name'],
        'location': scenario['location'],
        'alert_level': scenario['alert_level'],
        'timestamp': datetime.now().isoformat(),
        'risk_score': scenario['risk_score'],
        'sensor_data': scenario['sensor_data']
    }
    
    # Generate XAI explanation
    if alert_service.risk_explainer:
        risk_explanation = alert_service.risk_explainer.explain_risk_assessment(
            sensor_data=scenario['sensor_data'],
            risk_score=scenario['risk_score'],
            alert_level=scenario['alert_level'],
            historical_data=scenario['historical_data']
        )
        alert['risk_explanation'] = risk_explanation
    
    # Generate new XAI-enhanced SMS
    xai_sms = alert_service.generate_sms_body(alert)
    
    print("XAI-Enhanced SMS Alert:")
    print("-" * 30)
    print(xai_sms)
    print("-" * 30)
    print("✅ IMPROVEMENT: Shows specific sensor reading that triggered alert!")
    print("✅ IMPROVEMENT: Operators know exactly what's wrong!")
    
    return alert

def show_detailed_xai_analysis(alert):
    """Show the detailed XAI analysis that operators can access"""
    
    print(f"\n🤖 DETAILED XAI ANALYSIS - What Operators See in Dashboard/Email:")
    print("=" * 80)
    
    if not alert.get('risk_explanation'):
        print("❌ No XAI explanation available")
        return
    
    explanation = alert['risk_explanation']
    
    # Primary explanation
    print("🎯 PRIMARY EXPLANATION:")
    print("-" * 40)
    print(f"   {explanation['primary_explanation']}")
    print()
    
    # Contributing factors
    print("🔍 TOP CONTRIBUTING FACTORS:")
    print("-" * 40)
    for i, factor in enumerate(explanation['contributing_factors'][:4], 1):
        risk_level_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
        emoji = risk_level_emoji.get(factor['risk_level'], "⚪")
        print(f"   {i}. {emoji} {factor['factor'].title()}: {factor['current_value']}")
        print(f"      Risk Level: {factor['risk_level'].upper()}")
        print(f"      Contribution Score: {factor['contribution_score']:.1f}/10")
        print()
    
    # Threshold violations
    print("⚠️ THRESHOLD VIOLATIONS:")
    print("-" * 40)
    for violation in explanation['threshold_violations'][:3]:
        severity_emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡"}
        emoji = severity_emoji.get(violation['severity'], "⚪")
        print(f"   {emoji} {violation['sensor_type'].title()}:")
        print(f"      Current: {violation['current_value']:.1f}")
        print(f"      Threshold: {violation['threshold_value']:.1f}")
        print(f"      Exceeded by: {violation['percentage_over']:.1f}%")
        print()
    
    # AI Recommendations
    print("📋 AI-GENERATED RECOMMENDATIONS:")
    print("-" * 40)
    for i, rec in enumerate(explanation['recommendations'][:5], 1):
        print(f"   {i}. {rec}")
    print()
    
    # Confidence and reliability
    print("📊 SYSTEM CONFIDENCE:")
    print("-" * 40)
    confidence = explanation['confidence_level']
    confidence_emoji = "🟢" if confidence >= 80 else "🟡" if confidence >= 60 else "🔴"
    print(f"   {confidence_emoji} Assessment Confidence: {confidence}%")
    
    if confidence >= 80:
        print("   ✅ HIGH CONFIDENCE - Alert is highly reliable")
    elif confidence >= 60:
        print("   ⚠️ MEDIUM CONFIDENCE - Alert should be verified")
    else:
        print("   ❌ LOW CONFIDENCE - Manual inspection recommended")

def show_multilingual_xai_benefits():
    """Demonstrate multilingual XAI capabilities"""
    
    print(f"\n🌐 MULTILINGUAL XAI BENEFITS:")
    print("=" * 80)
    
    alert_service = AlertService()
    
    # Sample high-risk alert
    sample_alert = {
        'id': 'multilingual_demo',
        'mine_name': 'Odisha Iron Ore Mine',
        'location': 'Keonjhar, Odisha', 
        'alert_level': 'HIGH',
        'timestamp': datetime.now().isoformat(),
        'risk_score': 8.4,
        'sensor_data': {
            'vibration': 7.9,
            'acoustic': 94.2,
            'temperature': 41.8
        }
    }
    
    # Generate XAI explanation
    if alert_service.risk_explainer:
        risk_explanation = alert_service.risk_explainer.explain_risk_assessment(
            sensor_data=sample_alert['sensor_data'],
            risk_score=sample_alert['risk_score'],
            alert_level=sample_alert['alert_level']
        )
        sample_alert['risk_explanation'] = risk_explanation
    
    # Show different language versions
    language_demos = [
        (['hindi', 'english'], 'Hindi-speaking miners'),
        (['odia', 'hindi', 'english'], 'Odia-speaking local workers'), 
        (['bengali', 'hindi', 'english'], 'Bengali-speaking operators')
    ]
    
    for languages, audience in language_demos:
        print(f"\n📱 FOR {audience.upper()}:")
        print("-" * 50)
        sms_content = alert_service.generate_multilingual_sms(sample_alert, languages)
        lines = sms_content.split('\n')
        for line in lines[:4]:  # Show first 4 lines
            print(f"   {line}")
        print("   ...")
        print(f"   ✅ Workers understand alert in their native language!")

def demonstrate_real_world_scenario():
    """Show a complete real-world scenario"""
    
    print(f"\n🏭 REAL-WORLD SCENARIO DEMONSTRATION:")
    print("=" * 80)
    
    scenario = create_demo_high_risk_scenario()
    
    print("📍 SITUATION:")
    print(f"   Mine: {scenario['mine_name']}")
    print(f"   Location: {scenario['location']}")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Shift: {scenario['context']['shift']}")
    print(f"   Workers Present: {scenario['context']['workers_present']}")
    print(f"   Weather: {scenario['context']['weather_conditions']}")
    print()
    
    print("🚨 ALERT TRIGGERED:")
    print("   Risk Level: HIGH")
    print("   Risk Score: 8.7/10")
    print()
    
    print("🤖 AI ANALYSIS SHOWS:")
    print("   • Ground vibration at CRITICAL level (8.2 Hz vs 7.5 threshold)")
    print("   • Acoustic emissions at CRITICAL level (96.4 dB vs 80 threshold)")  
    print("   • Temperature rising to HIGH level (43.1°C vs 40 threshold)")
    print("   • Slope stability deteriorating (0.41 vs 0.3 threshold)")
    print("   • Upward trend in all risk factors over past 5 hours")
    print()
    
    print("💡 WHY THIS MATTERS:")
    print("   ❌ Old System: 'HIGH RISK - EVACUATE' (no explanation)")
    print("   ✅ New System: Workers see EXACTLY why there's danger")
    print("   ✅ Mine operators know which equipment/areas to check")
    print("   ✅ Faster, more informed decision-making")
    print("   ✅ Better compliance with safety protocols")
    print()
    
    print("⚡ IMMEDIATE ACTIONS RECOMMENDED BY AI:")
    print("   1. 🚨 EVACUATE workers from Block A immediately")
    print("   2. 🛑 STOP Excavator-01 and Drill-02 operations")
    print("   3. 🔍 INSPECT area around high vibration sensors")
    print("   4. 👂 INVESTIGATE acoustic emission sources") 
    print("   5. 📞 NOTIFY emergency response team")

def run_xai_demo():
    """Run the complete XAI demonstration"""
    
    print("🌟 EXPLAINABLE AI (XAI) ROCKFALL ALERT SYSTEM DEMO")
    print("🌟 Solving the 'Why is there high risk?' Problem")
    print("=" * 80)
    
    # Show before vs after
    enhanced_alert = demonstrate_before_vs_after()
    
    # Show detailed analysis
    show_detailed_xai_analysis(enhanced_alert)
    
    # Show multilingual benefits
    show_multilingual_xai_benefits()
    
    # Show real-world scenario
    demonstrate_real_world_scenario()
    
    print(f"\n{'='*80}")
    print("🎯 SUMMARY: XAI TRANSFORMS ROCKFALL SAFETY")
    print("=" * 80)
    print("\n🔍 BEFORE XAI:")
    print("   • Alerts said 'HIGH RISK' with no explanation")
    print("   • Mine operators confused about what to check")
    print("   • Slower response times due to uncertainty")
    print("   • Workers didn't understand reasoning behind evacuation")
    
    print("\n✨ AFTER XAI:")
    print("   • Clear explanation of WHY there's high risk")
    print("   • Specific sensor readings and thresholds exceeded")
    print("   • AI-generated step-by-step recommendations")
    print("   • Multilingual explanations for better understanding")
    print("   • Confidence levels help assess alert reliability")
    print("   • Faster, more informed safety decisions")
    
    print(f"\n🚀 RESULT: SAFER MINES THROUGH EXPLAINABLE AI!")
    print("=" * 80)

if __name__ == "__main__":
    run_xai_demo()
