#!/usr/bin/env python3
"""
WhatsApp Alert System - Integrated with Rockfall Prediction System
Provides reliable alert delivery when SMS fails due to carrier restrictions
"""

import os
import logging
from datetime import datetime, timedelta
from threading import Thread

try:
    import pywhatkit as pwk
    import pyautogui
    WHATSAPP_AVAILABLE = True
except ImportError:
    WHATSAPP_AVAILABLE = False
    print("WhatsApp feature not available. Install with: pip install pywhatkit pyautogui")

logger = logging.getLogger(__name__)

class WhatsAppService:
    """WhatsApp alert service for mining safety notifications"""
    
    def __init__(self):
        self.available = WHATSAPP_AVAILABLE
        self.default_wait_time = 15  # seconds
        self.tab_close = True
        
    def send_alert(self, phone_number, alert_data):
        """Send WhatsApp alert with mining-specific formatting"""
        if not self.available:
            return {'success': False, 'error': 'WhatsApp service not available'}
        
        try:
            # Format the alert message
            message = self._format_mining_alert(alert_data)
            
            # Send WhatsApp message
            result = self._send_whatsapp_message(phone_number, message)
            
            if result['success']:
                logger.info(f"WhatsApp alert sent to {phone_number} for mine {alert_data.get('mine_name', 'Unknown')}")
            
            return result
            
        except Exception as e:
            logger.error(f"WhatsApp alert failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _format_mining_alert(self, alert_data):
        """Format alert data into WhatsApp-friendly message"""
        mine_name = alert_data.get('mine_name', 'Unknown Mine')
        risk_level = alert_data.get('alert_level', 'UNKNOWN')
        risk_score = alert_data.get('risk_score', 'N/A')
        timestamp = datetime.now().strftime('%H:%M:%S, %d %b %Y')
        
        # Risk level emojis
        risk_emoji = {
            'HIGH': '🚨🔴',
            'MEDIUM': '⚠️🟡', 
            'LOW': '💚✅'
        }.get(risk_level, '⚠️')
        
        message = f"""{risk_emoji} *MINING SAFETY ALERT* {risk_emoji}

🏔️ *Mine:* {mine_name}
📊 *Risk Level:* {risk_level}
🎯 *Risk Score:* {risk_score}
⏰ *Time:* {timestamp}

*🚨 IMMEDIATE ACTION REQUIRED*

"""
        
        # Add XAI explanation if available
        if 'risk_explanation' in alert_data:
            explanation = alert_data['risk_explanation']
            if explanation.get('primary_explanation'):
                message += f"🤖 *AI Analysis:*\n{explanation['primary_explanation'][:200]}...\n\n"
            
            # Add top contributing factors
            factors = explanation.get('contributing_factors', [])
            if factors:
                message += "🔍 *Key Risk Factors:*\n"
                for factor in factors[:3]:
                    message += f"• {factor['factor'].title()}: {factor['current_value']} ({factor['risk_level']} level)\n"
                message += "\n"
            
            # Add recommendations
            recommendations = explanation.get('recommendations', [])
            if recommendations:
                message += "📋 *Recommended Actions:*\n"
                for i, rec in enumerate(recommendations[:3], 1):
                    message += f"{i}. {rec}\n"
                message += "\n"
        
        # Add emergency contacts
        message += "🆘 *Emergency:* Call 108\n"
        message += "🏗️ *System:* AI Rockfall Prediction\n"
        message += "📧 *Email alerts also sent*"
        
        return message
    
    def _send_whatsapp_message(self, phone_number, message):
        """Send WhatsApp message using pywhatkit"""
        try:
            # Clean phone number
            phone = self._clean_phone_number(phone_number)
            
            # Schedule message for immediate sending (1-2 minutes from now)
            now = datetime.now()
            send_time = now + timedelta(minutes=2)
            
            logger.info(f"Scheduling WhatsApp message to {phone} at {send_time.strftime('%H:%M')}")
            
            # Send via pywhatkit
            pwk.sendwhatmsg(
                phone_no=phone,
                message=message,
                time_hour=send_time.hour,
                time_min=send_time.minute,
                wait_time=self.default_wait_time,
                tab_close=self.tab_close
            )
            
            return {
                'success': True,
                'message': f'WhatsApp alert scheduled for {phone}',
                'scheduled_time': send_time.strftime('%H:%M'),
                'phone': phone
            }
            
        except Exception as e:
            logger.error(f"WhatsApp sending failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _clean_phone_number(self, phone_number):
        """Clean and format phone number for WhatsApp"""
        phone = phone_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        # Add country code if missing
        if not phone.startswith('+'):
            if phone.startswith('91'):
                phone = '+' + phone
            elif phone.startswith('7') or phone.startswith('8') or phone.startswith('9'):
                phone = '+91' + phone
            else:
                phone = '+91' + phone.replace('+91', '')
        
        return phone
    
    def send_test_message(self, phone_number):
        """Send test WhatsApp message"""
        test_alert = {
            'mine_name': 'Test Mine - Jharkhand',
            'alert_level': 'HIGH',
            'risk_score': 8.5,
            'sensor_data': {
                'vibration': 8.2,
                'acoustic': 95.0,
                'temperature': 42.0
            }
        }
        
        return self.send_alert(phone_number, test_alert)

# Legacy function for backward compatibility
def send_whatsapp_alert(phone_number, message):
    """Legacy function - use WhatsAppService class instead"""
    if not WHATSAPP_AVAILABLE:
        return {'success': False, 'error': 'pywhatkit not installed'}
    
    service = WhatsAppService()
    
    # Convert message to alert data format
    alert_data = {
        'mine_name': 'Legacy Alert',
        'alert_level': 'HIGH',
        'risk_score': 'N/A',
        'custom_message': message
    }
    
    return service.send_alert(phone_number, alert_data)

def test_whatsapp_alert():
    """Test WhatsApp alert functionality"""
    print("🧪 Testing WhatsApp Alert System")
    print("=" * 50)
    
    test_phone = '+917735776771'
    test_message = """🚨 ROCKFALL ALERT - TEST MESSAGE

Mine: Jharia Coalfield
Risk Level: HIGH
Risk Score: 8.5
Time: """ + datetime.datetime.now().strftime('%H:%M:%S') + """

This is a test alert from the AI-Based Rockfall Prediction System.

⚠️ In real emergency: Call 108
🏗️ System: AI Mining Safety Dashboard"""
    
    if not WHATSAPP_AVAILABLE:
        print("❌ WhatsApp not available. Install with:")
        print("   pip install pywhatkit")
        return False
    
    print(f"📱 Target: {test_phone}")
    print("📝 Message preview:")
    print(test_message[:100] + "...")
    
    confirm = input("\n⚠️  This will open WhatsApp Web and send a message. Continue? (y/N): ").strip().lower()
    
    if confirm == 'y':
        result = send_whatsapp_alert(test_phone, test_message)
        
        if result['success']:
            print(f"✅ WhatsApp alert scheduled successfully!")
            print(f"   Scheduled for: {result.get('scheduled_time', 'Now')}")
            print("   📱 Check your WhatsApp Web - it should open automatically")
            print("   ⏰ Message will be sent in ~1 minute")
        else:
            print(f"❌ WhatsApp alert failed: {result['error']}")
            
        return result['success']
    else:
        print("❌ WhatsApp test cancelled")
        return False

if __name__ == "__main__":
    test_whatsapp_alert()