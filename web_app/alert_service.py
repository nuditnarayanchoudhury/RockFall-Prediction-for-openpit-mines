import json
import requests
from datetime import datetime, timedelta
import smtplib
try:
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
except ImportError:
    # Fallback for email functionality
    MIMEText = None
    MIMEMultipart = None
import os

try:
    from twilio.rest import Client
except ImportError:
    # Fallback if Twilio is not installed
    Client = None

try:
    from risk_explainer import RockfallRiskExplainer
except ImportError:
    RockfallRiskExplainer = None

try:
    from whatsapp_alert import WhatsAppService
except ImportError:
    WhatsAppService = None

class AlertService:
    def __init__(self):
        self.active_alerts = []
        self.alert_thresholds = {
            'HIGH': 0.7,
            'MEDIUM': 0.4,
            'LOW': 0.0
        }
        
        # Initialize XAI Risk Explainer
        self.risk_explainer = RockfallRiskExplainer() if RockfallRiskExplainer else None
        
        # Initialize WhatsApp service
        self.whatsapp_service = WhatsAppService() if WhatsAppService else None
        
        # Email configuration
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_user = os.getenv('EMAIL_USER', '')
        self.email_password = os.getenv('EMAIL_PASSWORD', '')
        
        # SMS configuration (Twilio)
        self.twilio_sid = os.getenv('TWILIO_SID', '')
        self.twilio_token = os.getenv('TWILIO_TOKEN', '')
        self.twilio_phone = os.getenv('TWILIO_PHONE', '')
        
        # Alert recipients
        self.alert_recipients = self.load_alert_recipients()
        
    def load_alert_recipients(self):
        """Load alert recipients from configuration"""
        # Load from environment variables with fallback defaults
        emergency_emails = os.getenv('EMERGENCY_EMAILS', 'emergency@mining-authority.gov.in,safety@company.com').split(',') 
        manager_emails = os.getenv('MANAGER_EMAILS', 'manager1@company.com,manager2@company.com').split(',')
        operator_emails = os.getenv('OPERATOR_EMAILS', 'ops1@company.com,ops2@company.com').split(',')
        
        emergency_phones = os.getenv('EMERGENCY_PHONES', '+917735776771,+919078280686').split(',')
        manager_phones = os.getenv('MANAGER_PHONES', '+917735776771,+919078280686').split(',')
        operator_phones = os.getenv('OPERATOR_PHONES', '+917735776771,+919078280686').split(',')
        
        return {
            'emergency': {
                'emails': [email.strip() for email in emergency_emails if email.strip()],
                'phones': [phone.strip() for phone in emergency_phones if phone.strip()]
            },
            'managers': {
                'emails': [email.strip() for email in manager_emails if email.strip()],
                'phones': [phone.strip() for phone in manager_phones if phone.strip()]
            },
            'operators': {
                'emails': [email.strip() for email in operator_emails if email.strip()],
                'phones': [phone.strip() for phone in operator_phones if phone.strip()]
            }
        }
    
    def send_alert(self, mine_id, alert_level, risk_data=None):
        """Send alert via multiple channels"""
        from data_service import DataService
        data_service = DataService()
        
        mine = data_service.get_mine_by_id(mine_id)
        if not mine:
            return {'success': False, 'error': 'Mine not found'}
        
        alert_id = f"alert_{mine_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        alert = {
            'id': alert_id,
            'mine_id': mine_id,
            'mine_name': mine['name'],
            'location': mine['location'],
            'alert_level': alert_level,
            'timestamp': datetime.now().isoformat(),
            'status': 'ACTIVE',
            'channels_used': []
        }
        
        # Add risk data if provided
        if risk_data:
            alert['risk_score'] = risk_data.get('risk_score', 0)
            alert['key_factors'] = risk_data.get('key_factors', [])
            alert['sensor_data'] = risk_data.get('sensor_data', {})
            
            # Generate XAI explanation if risk explainer is available
            if self.risk_explainer and alert['sensor_data']:
                risk_explanation = self.risk_explainer.explain_risk_assessment(
                    sensor_data=alert['sensor_data'],
                    risk_score=alert['risk_score'],
                    alert_level=alert_level,
                    historical_data=risk_data.get('historical_data')
                )
                alert['risk_explanation'] = risk_explanation
        
        success_count = 0
        total_attempts = 0
        
        # Determine recipients based on alert level
        if alert_level == 'HIGH':
            recipients = ['emergency', 'managers', 'operators']
        elif alert_level == 'MEDIUM':
            recipients = ['managers', 'operators']
        else:
            recipients = ['operators']
        
        # Send email alerts
        email_result = self.send_email_alert(alert, recipients)
        if email_result['success']:
            success_count += 1
            alert['channels_used'].append('EMAIL')
        total_attempts += 1
        
        # Send SMS alerts for HIGH priority only
        if alert_level == 'HIGH':
            sms_result = self.send_sms_alert(alert, recipients)
            if sms_result['success']:
                success_count += 1
                alert['channels_used'].append('SMS')
            else:
                # If SMS fails, try WhatsApp as fallback
                whatsapp_result = self.send_whatsapp_alert(alert, recipients)
                if whatsapp_result['success']:
                    success_count += 1
                    alert['channels_used'].append('WHATSAPP')
            total_attempts += 1
        
        # Store alert in active alerts
        self.active_alerts.append(alert)
        
        # Clean up old alerts (keep only last 24 hours)
        self.cleanup_old_alerts()
        
        return {
            'success': success_count > 0,
            'alert_id': alert_id,
            'channels_used': alert['channels_used'],
            'recipients_count': len(recipients),
            'success_rate': success_count / total_attempts if total_attempts > 0 else 0
        }
    
    def send_email_alert(self, alert, recipient_groups):
        """Send email alert"""
        try:
            if MIMEText is None or MIMEMultipart is None:
                print("Email modules not available")
                return {'success': False, 'error': 'Email modules not installed'}
                
            if not self.email_user or not self.email_password:
                print("Email credentials not configured")
                return {'success': False, 'error': 'Email not configured'}
            
            # Collect all email addresses
            emails = []
            for group in recipient_groups:
                emails.extend(self.alert_recipients.get(group, {}).get('emails', []))
            
            if not emails:
                return {'success': False, 'error': 'No email recipients'}
            
            # Create bilingual email content
            hindi_risk = {'HIGH': 'अत्यधिक खतरा', 'MEDIUM': 'मध्यम खतरा', 'LOW': 'कम खतरा'}.get(alert['alert_level'], 'खतरा')
            subject = f"🚨 शिलाखंड अलर्ट | ROCKFALL ALERT - {hindi_risk} | {alert['alert_level']} RISK - {alert['mine_name']}"
            
            body = self.generate_email_body(alert)
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = ', '.join(emails)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            return {'success': True, 'recipients': len(emails)}
            
        except Exception as e:
            print(f"Error sending email alert: {e}")
            return {'success': False, 'error': str(e)}
    
    def send_sms_alert(self, alert, recipient_groups):
        """Send SMS alert using Twilio with error handling and fallbacks"""
        try:
            if Client is None:
                print("Twilio SMS module not available")
                return {'success': False, 'error': 'Twilio not installed'}
                
            if not self.twilio_sid or not self.twilio_token:
                print("SMS credentials not configured")
                return {'success': False, 'error': 'SMS not configured'}
            
            client = Client(self.twilio_sid, self.twilio_token)
            
            # Collect all phone numbers
            phones = []
            for group in recipient_groups:
                phones.extend(self.alert_recipients.get(group, {}).get('phones', []))
            
            if not phones:
                return {'success': False, 'error': 'No phone recipients'}
            
            # Try multiple message formats for better delivery
            message_formats = [
                self.generate_sms_body(alert),  # Full multilingual message
                self.generate_simple_sms_body(alert),  # Shorter English message
                self.generate_minimal_sms_body(alert)   # Minimal alert
            ]
            
            sent_count = 0
            failed_count = 0
            error_details = []
            
            for phone in phones:
                message_sent = False
                
                # Try different message formats
                for i, message_body in enumerate(message_formats):
                    try:
                        message = client.messages.create(
                            body=message_body,
                            from_=self.twilio_phone,
                            to=phone
                        )
                        
                        # Check if message was sent successfully
                        if message.status in ['queued', 'sent', 'delivered']:
                            sent_count += 1
                            message_sent = True
                            print(f"SMS sent successfully to {phone} (format {i+1})")
                            break
                        else:
                            print(f"SMS failed to {phone}: Status {message.status}")
                            
                    except Exception as e:
                        error_msg = str(e)
                        print(f"SMS attempt {i+1} failed to {phone}: {error_msg}")
                        
                        # Check for specific error codes
                        if '30044' in error_msg:
                            error_details.append(f"Carrier blocked SMS to {phone} (Error 30044)")
                        elif '21211' in error_msg:
                            error_details.append(f"Invalid phone number: {phone}")
                        else:
                            error_details.append(f"SMS error to {phone}: {error_msg}")
                
                if not message_sent:
                    failed_count += 1
            
            # Determine overall success
            success = sent_count > 0
            
            result = {
                'success': success,
                'recipients': sent_count,
                'failed': failed_count,
                'total_attempted': len(phones)
            }
            
            if error_details:
                result['error_details'] = error_details
                result['common_errors'] = self._analyze_common_errors(error_details)
            
            # If all SMS failed, suggest alternatives
            if not success:
                result['suggestions'] = [
                    "Try using an Indian SMS provider (MSG91, TextLocal)",
                    "Use WhatsApp API for better delivery",
                    "Upgrade Twilio account from Trial to Paid",
                    "Email alerts are working as fallback"
                ]
            
            return result
            
        except Exception as e:
            print(f"Error sending SMS alerts: {e}")
            return {'success': False, 'error': str(e)}
    
    def generate_simple_sms_body(self, alert):
        """Generate shorter SMS message for better delivery"""
        return f"""MINING ALERT: {alert['alert_level']} risk at {alert['mine_name']}. Score: {alert.get('risk_score', 'N/A')}. Time: {datetime.fromisoformat(alert['timestamp']).strftime('%H:%M')}. Immediate action required."""
    
    def generate_minimal_sms_body(self, alert):
        """Generate minimal SMS message"""
        return f"ALERT: {alert['alert_level']} risk - {alert['mine_name']} - {alert.get('risk_score', 'N/A')}"
    
    def _analyze_common_errors(self, error_details):
        """Analyze common SMS errors and provide insights"""
        errors = ' '.join(error_details).lower()
        
        if '30044' in errors:
            return "Carrier blocking detected. Consider using Indian SMS provider or upgrading Twilio account."
        elif 'invalid' in errors:
            return "Phone number format issues detected. Check number formatting."
        elif 'trial' in errors:
            return "Trial account limitations. Consider upgrading to paid Twilio account."
        else:
            return "Mixed SMS delivery issues. Check network and carrier settings."
    
    def send_whatsapp_alert(self, alert, recipient_groups):
        """Send WhatsApp alert as SMS fallback"""
        if not self.whatsapp_service or not self.whatsapp_service.available:
            return {'success': False, 'error': 'WhatsApp service not available'}
        
        try:
            # Collect all phone numbers
            phones = []
            for group in recipient_groups:
                phones.extend(self.alert_recipients.get(group, {}).get('phones', []))
            
            if not phones:
                return {'success': False, 'error': 'No phone recipients for WhatsApp'}
            
            sent_count = 0
            errors = []
            
            # Send WhatsApp to each recipient
            for phone in phones:
                try:
                    result = self.whatsapp_service.send_alert(phone, alert)
                    if result['success']:
                        sent_count += 1
                        print(f"WhatsApp alert sent to {phone}")
                    else:
                        errors.append(f"WhatsApp failed for {phone}: {result.get('error', 'Unknown')}")
                except Exception as e:
                    errors.append(f"WhatsApp error for {phone}: {str(e)}")
            
            success = sent_count > 0
            result = {
                'success': success,
                'recipients': sent_count,
                'total_attempted': len(phones)
            }
            
            if errors:
                result['errors'] = errors
                result['error_summary'] = f"{len(errors)} WhatsApp delivery issues"
            
            return result
            
        except Exception as e:
            print(f"WhatsApp alert service error: {e}")
            return {'success': False, 'error': str(e)}
    
    def send_whatsapp_test(self, phone_number):
        """Send test WhatsApp message"""
        if not self.whatsapp_service or not self.whatsapp_service.available:
            return {'success': False, 'error': 'WhatsApp service not available'}
        
        try:
            result = self.whatsapp_service.send_test_message(phone_number)
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generate_email_body(self, alert):
        """Generate bilingual HTML email body (Hindi + English)"""
        risk_color = {'HIGH': '#dc3545', 'MEDIUM': '#ffc107', 'LOW': '#28a745'}.get(alert['alert_level'], '#6c757d')
        hindi_risk = {'HIGH': 'अत्यधिक खतरा', 'MEDIUM': 'मध्यम खतरा', 'LOW': 'कम खतरा'}.get(alert['alert_level'], 'खतरा')
        
        # Generate XAI explanation section
        explanation_html = ''
        factors_html = ''
        
        if alert.get('risk_explanation'):
            explanation = alert['risk_explanation']
            
            # Primary explanation
            if explanation.get('primary_explanation'):
                explanation_html += f'<div class="explanation"><h3>🤖 AI Risk Analysis | AI जोखिम विश्लेषण</h3>'
                explanation_html += f'<p><strong>{explanation["primary_explanation"]}</strong></p></div>'
            
            # Contributing factors with detailed analysis
            if explanation.get('contributing_factors'):
                factors_html = '<div class="factors"><h3>🔍 Key Contributing Factors | मुख्य योगदान कारक</h3><ul>'
                for factor in explanation['contributing_factors'][:3]:  # Top 3 factors
                    factors_html += f'<li><strong>{factor["factor"].title()}:</strong> {factor["current_value"]} ({factor["risk_level"]} level) - Score: {factor["contribution_score"]:.1f}</li>'
                factors_html += '</ul></div>'
            
            # Threshold violations
            if explanation.get('threshold_violations'):
                violations_html = '<div class="violations"><h3>⚠️ Threshold Violations | सीमा उल्लंघन</h3><ul>'
                for violation in explanation['threshold_violations'][:3]:  # Top 3 violations
                    violations_html += f'<li><strong>{violation["sensor_type"].title()}:</strong> {violation["current_value"]:.1f} (Threshold: {violation["threshold_value"]:.1f}) - {violation["percentage_over"]:.1f}% over limit</li>'
                violations_html += '</ul></div>'
                explanation_html += violations_html
            
            # Recommendations
            if explanation.get('recommendations'):
                recommendations_html = '<div class="recommendations"><h3>📋 AI Recommendations | AI सिफारिशें</h3><ul>'
                for rec in explanation['recommendations'][:5]:  # Top 5 recommendations
                    recommendations_html += f'<li>{rec}</li>'
                recommendations_html += '</ul></div>'
                explanation_html += recommendations_html
        
        # Fallback to legacy key factors if no XAI explanation
        elif alert.get('key_factors'):
            factors_html = '<div class="factors"><h3>Key Risk Factors</h3><ul>' + ''.join([f'<li>{factor}</li>' for factor in alert['key_factors']]) + '</ul></div>'
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
                .header {{ background-color: {risk_color}; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .mine-info {{ background-color: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .explanation {{ background-color: #e7f3ff; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007bff; }}
                .factors {{ background-color: #fff3cd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .violations {{ background-color: #f8d7da; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .recommendations {{ background-color: #d4edda; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #dee2e6; color: #6c757d; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚨 शिलाखंड जोखिम अलर्ट | ROCKFALL RISK ALERT</h1>
                <h2>{hindi_risk} | {alert['alert_level']} RISK DETECTED</h2>
                <h3>खतरा मिला | खतरा का पता चला</h3>
            </div>
            
            <div class="content">
                <div class="mine-info">
                    <h3>खान की जानकारी | Mine Information</h3>
                    <p><strong>खान | Mine:</strong> {alert['mine_name']}</p>
                    <p><strong>स्थान | Location:</strong> {alert['location']}</p>
                    <p><strong>अलर्ट समय | Alert Time:</strong> {datetime.fromisoformat(alert['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>जोखिम स्कोर | Risk Score:</strong> {alert.get('risk_score', 'N/A')}</p>
                </div>
                
                {explanation_html}
                {factors_html}
                
                <div class="actions">
                    <h3>तत्काल आवश्यक कार्य | Immediate Actions Required:</h3>
                    {self.get_action_recommendations_bilingual(alert['alert_level'])}
                </div>
            </div>
            
            <div class="footer">
                <p>यह AI-आधारित शिलाखंड भविष्यवाणी सिस्टम से एक स्वचालित अलर्ट है | This is an automated alert from the AI-Based Rockfall Prediction System.</p>
                <p>आपातकालीन स्थितियों के लिए संपर्क करें | For emergency situations, contact: Emergency Services - 108</p>
            </div>
        </body>
        </html>
        """
    
    def generate_sms_body(self, alert):
        """Generate area-based multilingual SMS alert body"""
        # Get mine location and determine appropriate languages
        mine_location = alert.get('location', '')
        mine_state = self.extract_state_from_location(mine_location)
        
        # Get area-based language configuration
        languages = self.get_area_languages(mine_state)
        
        # Generate message in appropriate regional languages + English
        return self.generate_multilingual_sms(alert, languages)
    
    def extract_state_from_location(self, location):
        """Extract state from mine location string"""
        state_mapping = {
            'jharkhand': 'JHARKHAND',
            'odisha': 'ODISHA', 
            'chhattisgarh': 'CHHATTISGARH',
            'west bengal': 'WEST_BENGAL',
            'rajasthan': 'RAJASTHAN',
            'gujarat': 'GUJARAT',
            'maharashtra': 'MAHARASHTRA',
            'karnataka': 'KARNATAKA',
            'telangana': 'TELANGANA',
            'andhra pradesh': 'ANDHRA_PRADESH',
            'madhya pradesh': 'MADHYA_PRADESH'
        }
        
        location_lower = location.lower()
        for state_key, state_code in state_mapping.items():
            if state_key in location_lower:
                return state_code
        
        return 'DEFAULT'  # Fallback to Hindi + English
    
    def get_area_languages(self, state):
        """Get appropriate languages for each mining area/state"""
        area_languages = {
            'JHARKHAND': ['hindi', 'english'],  # Hindi is widely understood
            'ODISHA': ['odia', 'hindi', 'english'],  # Odia + Hindi + English
            'CHHATTISGARH': ['hindi', 'english'],  # Hindi is primary
            'WEST_BENGAL': ['bengali', 'hindi', 'english'],  # Bengali + Hindi + English
            'RAJASTHAN': ['hindi', 'english'],  # Hindi is primary
            'GUJARAT': ['gujarati', 'hindi', 'english'],  # Gujarati + Hindi + English
            'MAHARASHTRA': ['marathi', 'hindi', 'english'],  # Marathi + Hindi + English
            'KARNATAKA': ['kannada', 'hindi', 'english'],  # Kannada + Hindi + English
            'TELANGANA': ['telugu', 'hindi', 'english'],  # Telugu + Hindi + English
            'ANDHRA_PRADESH': ['telugu', 'hindi', 'english'],  # Telugu + Hindi + English
            'MADHYA_PRADESH': ['hindi', 'english'],  # Hindi is primary
            'DEFAULT': ['hindi', 'english']  # Default fallback
        }
        
        return area_languages.get(state, ['hindi', 'english'])
    
    def generate_multilingual_sms(self, alert, languages):
        """Generate SMS with appropriate regional languages and XAI explanations"""
        # Language-specific translations
        translations = self.get_language_translations()
        
        # Build message parts in each language
        message_parts = []
        
        # Add emoji and main alert header
        message_parts.append("🚨 " + " | ".join([translations[lang]['alert_header'] for lang in languages]))
        message_parts.append("")
        
        # Mine information
        mine_labels = [translations[lang]['mine'] for lang in languages]
        message_parts.append(" | ".join(mine_labels) + f": {alert['mine_name']}")
        
        # Risk level
        risk_translations = [translations[lang]['risk_levels'].get(alert['alert_level'], alert['alert_level']) for lang in languages]
        risk_labels = [translations[lang]['risk'] for lang in languages]
        message_parts.append(" | ".join(risk_labels) + ": " + " | ".join(risk_translations))
        
        # Add XAI explanation if available
        if alert.get('risk_explanation'):
            explanation = alert['risk_explanation']
            if explanation.get('primary_explanation'):
                # Extract key contributing factors for SMS (keep it concise)
                contributing_factors = explanation.get('contributing_factors', [])
                if contributing_factors:
                    top_factor = contributing_factors[0]
                    factor_desc = self.get_multilingual_factor_description(top_factor, languages)
                    message_parts.append(f"📊 {factor_desc}")
        
        # Time
        time_labels = [translations[lang]['time'] for lang in languages]
        time_str = datetime.fromisoformat(alert['timestamp']).strftime('%H:%M')
        message_parts.append(" | ".join(time_labels) + f": {time_str}")
        
        # Score
        score_labels = [translations[lang]['score'] for lang in languages]
        message_parts.append(" | ".join(score_labels) + f": {alert.get('risk_score', 'N/A')}")
        
        message_parts.append("")
        
        # Actions based on risk level
        action_text = self.get_multilingual_actions(alert['alert_level'], languages)
        message_parts.append(action_text)
        
        message_parts.append("")
        
        # System signature
        system_labels = [translations[lang]['system_name'] for lang in languages]
        message_parts.append("- " + " | ".join(system_labels))
        
        return "\n".join(message_parts)
    
    def get_language_translations(self):
        """Comprehensive language translations for Indian mining regions"""
        return {
            'hindi': {
        'alert_header': 'शिलाखंड अलर्ट (Rockfall Alert)',
        'mine': 'खान (Mine)',
        'risk': 'जोखिम (Risk)',
        'time': 'समय (Time)',
        'score': 'स्कोर (Score)',
        'system_name': 'AI शिलाखंड सिस्टम (AI Rockfall System)',
        'risk_levels': {
            'HIGH': 'उच्च जोखिम (HIGH RISK)',
            'MEDIUM': 'मध्यम जोखिम (MEDIUM RISK)',
            'LOW': 'निम्न जोखिम (LOW RISK)'
        },
        'actions': {
            'HIGH': 'तुरंत निकासी करें! ऑपरेशन बंद करें! (EVACUATE NOW! Stop operations!)',
            'MEDIUM': 'प्रवेश प्रतिबंधित करें। निगरानी बढ़ाएं। (Restrict access. Increase monitoring.)',
            'LOW': 'सावधानी बरतें। निगरानी जारी रखें। (Continue with caution. Monitor closely.)'
        }
    },
            'english': {
                'alert_header': 'ROCKFALL ALERT',
                'mine': 'Mine',
                'risk': 'Risk',
                'time': 'Time', 
                'score': 'Score',
                'system_name': 'AI Rockfall System',
                'risk_levels': {
                    'HIGH': 'HIGH RISK',
                    'MEDIUM': 'MEDIUM RISK',
                    'LOW': 'LOW RISK'
                },
                'actions': {
                    'HIGH': 'EVACUATE NOW! Stop operations!',
                    'MEDIUM': 'Restrict access. Increase monitoring.',
                    'LOW': 'Continue with caution. Monitor closely.'
                }
            },
            'bengali': {
                'alert_header': 'শিলাপতন সতর্কতা',
                'mine': 'খনি',
                'risk': 'ঝুঁকি',
                'time': 'সময়',
                'score': 'স্কোর',
                'system_name': 'AI শিলাপতন সিস্টেম',
                'risk_levels': {
                    'HIGH': 'উচ্চ ঝুঁকি',
                    'MEDIUM': 'মধ্যম ঝুঁকি',
                    'LOW': 'কম ঝুঁকি'
                },
                'actions': {
                    'HIGH': 'এখনই সরে যান! কাজ বন্ধ করুন!',
                    'MEDIUM': 'প্রবেশ সীমিত করুন। নিরীক্ষণ বাড়ান।',
                    'LOW': 'সতর্ক থাকুন। নিরীক্ষণ চালিয়ে যান।'
                }
            },
            'odia': {
                'alert_header': 'ପଥର ଖସିବା ଚେତାବନୀ',
                'mine': 'ଖଣି',
                'risk': 'ବିପଦ',
                'time': 'ସମୟ',
                'score': 'ସ୍କୋର',
                'system_name': 'AI ପଥର ଖସିବା ସିଷ୍ଟମ',
                'risk_levels': {
                    'HIGH': 'ଅଧିକ ବିପଦ',
                    'MEDIUM': 'ମଧ୍ୟମ ବିପଦ',
                    'LOW': 'କମ ବିପଦ'
                },
                'actions': {
                    'HIGH': 'ତତକ୍ଷଣାତ ବାହାରିଯାଆନ୍ତୁ! କାମ ବନ୍ଦ କରନ୍ତୁ!',
                    'MEDIUM': 'ପ୍ରବେଶ ସୀମିତ କରନ୍ତୁ। ନିରୀକ୍ଷଣ ବଢ଼ାନ୍ତୁ।',
                    'LOW': 'ସତର୍କ ରୁହନ୍ତୁ। ନିରୀକ୍ଷଣ ଜାରି ରଖନ୍ତୁ।'
                }
            },
            'gujarati': {
                'alert_header': 'ખડક પતન ચેતવણી',
                'mine': 'ખાણ',
                'risk': 'જોખમ',
                'time': 'સમય',
                'score': 'સ્કોર',
                'system_name': 'AI ખડક પતન સિસ્ટમ',
                'risk_levels': {
                    'HIGH': 'વધુ જોખમ',
                    'MEDIUM': 'મધ્યમ જોખમ',
                    'LOW': 'ઓછું જોખમ'
                },
                'actions': {
                    'HIGH': 'તુરંત બહાર નીકળો! કામ બંધ કરો!',
                    'MEDIUM': 'પ્રવેશ મર્યાદિત કરો। દેખરેખ વધારો।',
                    'LOW': 'સાવધાન રહો। દેખરેખ ચાલુ રાખો।'
                }
            },
            'marathi': {
                'alert_header': 'खडक कोसळण्याची सूचना',
                'mine': 'खाण',
                'risk': 'धोका',
                'time': 'वेळ',
                'score': 'स्कोअर',
                'system_name': 'AI खडक कोसळणे सिस्टम',
                'risk_levels': {
                    'HIGH': 'अधिक धोका',
                    'MEDIUM': 'मध्यम धोका',
                    'LOW': 'कमी धोका'
                },
                'actions': {
                    'HIGH': 'ताबडतोब बाहेर पडा! काम बंद करा!',
                    'MEDIUM': 'प्रवेश मर्यादित करा। देखरेख वाढवा।',
                    'LOW': 'सावध राहा। देखरेख चालू ठेवा।'
                }
            },
            'kannada': {
                'alert_header': 'ಬಂಡೆ ಕುಸಿತ ಎಚ್ಚರಿಕೆ',
                'mine': 'ಗಣಿ',
                'risk': 'ಅಪಾಯ',
                'time': 'ಸಮಯ',
                'score': 'ಸ್ಕೋರ್',
                'system_name': 'AI ಬಂಡೆ ಕುಸಿತ ಸಿಸ್ಟಂ',
                'risk_levels': {
                    'HIGH': 'ಹೆಚ್ಚು ಅಪಾಯ',
                    'MEDIUM': 'ಮಧ್ಯಮ ಅಪಾಯ',
                    'LOW': 'ಕಡಿಮೆ ಅಪಾಯ'
                },
                'actions': {
                    'HIGH': 'ತಕ್ಷಣವೇ ಹೊರಬರಿ! ಕೆಲಸ ನಿಲ್ಲಿಸಿ!',
                    'MEDIUM': 'ಪ್ರವೇಶ ಸೀಮಿತಗೊಳಿಸಿ। ಮೇಲ್ವಿಚಾರಣೆ ಹೆಚ್ಚಿಸಿ।',
                    'LOW': 'ಎಚ್ಚರದಿಂದಿರಿ। ಮೇಲ್ವಿಚಾರಣೆ ಮುಂದುವರಿಸಿ।'
                }
            },
            'telugu': {
                'alert_header': 'రాతిపటన హెచ్చరిక',
                'mine': 'గని',
                'risk': 'ప్రమాదం',
                'time': 'సమయం',
                'score': 'స్కోర్',
                'system_name': 'AI రాతిపటన వ్యవస్థ',
                'risk_levels': {
                    'HIGH': 'ఎక్కువ ప్రమాదం',
                    'MEDIUM': 'మధ్యమ ప్రమాదం',
                    'LOW': 'తక్కువ ప్రమాదం'
                },
                'actions': {
                    'HIGH': 'వెంటనే బయటకు వెళ్లండి! పని ఆపండి!',
                    'MEDIUM': 'ప్రవేశం పరిమితం చేయండి। పర్యవేక్షణ పెంచండి।',
                    'LOW': 'జాగ్రత్తగా ఉండండి। పర్యవేక్షణ కొనసాగించండి।'
                }
            }
        }
    
    def get_multilingual_actions(self, alert_level, languages):
        """Get action instructions in multiple languages"""
        translations = self.get_language_translations()
        action_texts = []
        
        for lang in languages:
            if lang in translations:
                action = translations[lang]['actions'].get(alert_level, 'Monitor situation')
                action_texts.append(action)
        
        return " | ".join(action_texts)
    
    def get_multilingual_factor_description(self, factor, languages):
        """Generate multilingual description for risk factors"""
        factor_translations = {
            'english': {
                'vibration': f"Vibration: {factor['current_value']:.1f}Hz",
                'temperature': f"Temp: {factor['current_value']:.1f}°C", 
                'humidity': f"Humidity: {factor['current_value']:.1f}%",
                'pressure': f"Pressure: {factor['current_value']:.1f}hPa",
                'acoustic': f"Sound: {factor['current_value']:.1f}dB",
                'slope_stability': f"Slope: {factor['current_value']:.2f}"
            },
            'hindi': {
                'vibration': f"कंपन: {factor['current_value']:.1f}Hz",
                'temperature': f"तापमान: {factor['current_value']:.1f}°C",
                'humidity': f"नमी: {factor['current_value']:.1f}%", 
                'pressure': f"दबाव: {factor['current_value']:.1f}hPa",
                'acoustic': f"ध्वनि: {factor['current_value']:.1f}dB",
                'slope_stability': f"ढलान: {factor['current_value']:.2f}"
            },
            'bengali': {
                'vibration': f"কম্পন: {factor['current_value']:.1f}Hz",
                'temperature': f"তাপমাত্রা: {factor['current_value']:.1f}°C",
                'humidity': f"আর্দ্রতা: {factor['current_value']:.1f}%",
                'pressure': f"চাপ: {factor['current_value']:.1f}hPa",
                'acoustic': f"শব্দ: {factor['current_value']:.1f}dB",
                'slope_stability': f"ঢাল: {factor['current_value']:.2f}"
            },
            'odia': {
                'vibration': f"କମ୍ପନ: {factor['current_value']:.1f}Hz",
                'temperature': f"ତାପମାତ୍ରା: {factor['current_value']:.1f}°C",
                'humidity': f"ଆର୍ଦ୍ରତା: {factor['current_value']:.1f}%",
                'pressure': f"ଚାପ: {factor['current_value']:.1f}hPa",
                'acoustic': f"ଧ୍ବନି: {factor['current_value']:.1f}dB",
                'slope_stability': f"ଢାଲୁ: {factor['current_value']:.2f}"
            }
            # Add more language translations as needed
        }
        
        factor_type = factor['factor']
        descriptions = []
        
        for lang in languages:
            if lang in factor_translations and factor_type in factor_translations[lang]:
                descriptions.append(factor_translations[lang][factor_type])
        
        return " | ".join(descriptions)
    
    def get_action_recommendations(self, alert_level):
        """Get HTML formatted action recommendations (English only - for backwards compatibility)"""
        if alert_level == 'HIGH':
            return """
            <ul>
                <li><strong>IMMEDIATELY evacuate all personnel from high-risk areas</strong></li>
                <li>Stop all mining operations in affected zones</li>
                <li>Deploy emergency response teams</li>
                <li>Activate emergency communication protocols</li>
                <li>Contact local authorities and emergency services</li>
                <li>Increase monitoring sensor frequency</li>
            </ul>
            """
        elif alert_level == 'MEDIUM':
            return """
            <ul>
                <li>Restrict access to potentially unstable areas</li>
                <li>Increase monitoring frequency</li>
                <li>Review and update safety protocols</li>
                <li>Brief all personnel on current risk status</li>
                <li>Prepare evacuation procedures</li>
            </ul>
            """
        else:
            return """
            <ul>
                <li>Continue normal operations with standard precautions</li>
                <li>Maintain regular monitoring schedule</li>
                <li>Monitor for any changes in conditions</li>
            </ul>
            """
    
    def get_action_recommendations_bilingual(self, alert_level):
        """Get HTML formatted action recommendations in both Hindi and English"""
        if alert_level == 'HIGH':
            return """
            <ul>
                <li><strong>तुरंत सभी कर्मचारियों को उच्च जोखिम वाले क्षेत्रों से हटाएं | IMMEDIATELY evacuate all personnel from high-risk areas</strong></li>
                <li>प्रभावित क्षेत्रों में सभी खनन काम बंद करें | Stop all mining operations in affected zones</li>
                <li>आपातकालीन प्रतिक्रिया टीम तैनात करें | Deploy emergency response teams</li>
                <li>आपातकालीन संचार प्रोटोकॉल सक्रिय करें | Activate emergency communication protocols</li>
                <li>स्थानीय अधिकारियों और आपातकालीन सेवाओं से संपर्क करें | Contact local authorities and emergency services</li>
                <li>निगरानी सेंसर की आवृत्ति बढ़ाएं | Increase monitoring sensor frequency</li>
            </ul>
            """
        elif alert_level == 'MEDIUM':
            return """
            <ul>
                <li>संभावित रूप से अस्थिर क्षेत्रों में प्रवेश प्रतिबंधित करें | Restrict access to potentially unstable areas</li>
                <li>निगरानी की आवृत्ति बढ़ाएं | Increase monitoring frequency</li>
                <li>सुरक्षा प्रोटोकॉल की समीक्षा और अपडेट करें | Review and update safety protocols</li>
                <li>वर्तमान जोखिम स्थिति पर सभी कर्मचारियों को जानकारी दें | Brief all personnel on current risk status</li>
                <li>निकासी प्रक्रियाओं की तैयारी करें | Prepare evacuation procedures</li>
            </ul>
            """
        else:
            return """
            <ul>
                <li>मानक सावधानियों के साथ सामान्य परिचालन जारी रखें | Continue normal operations with standard precautions</li>
                <li>नियमित निगरानी कार्यक्रम बनाए रखें | Maintain regular monitoring schedule</li>
                <li>स्थितियों में किसी भी बदलाव पर नजर रखें | Monitor for any changes in conditions</li>
            </ul>
            """
    
    def get_sms_action(self, alert_level):
        """Get brief SMS action text (English only - for backwards compatibility)"""
        if alert_level == 'HIGH':
            return "EVACUATE NOW! Stop operations."
        elif alert_level == 'MEDIUM':
            return "Restrict access. Increase monitoring."
        else:
            return "Continue with caution."
    
    def get_sms_action_bilingual(self, alert_level):
        """Get brief SMS action text in both Hindi and English"""
        if alert_level == 'HIGH':
            return """तुरंत निकासी करें! | EVACUATE NOW!
ऑपरेशन बंद करें | Stop operations!
आपातकाल प्रक्रिया शुरू करें | Start emergency protocol!"""
        elif alert_level == 'MEDIUM':
            return """प्रवेश प्रतिबंधित करें | Restrict access
निगरानी बढ़ाएं | Increase monitoring
तैयार रहें | Stay prepared"""
        else:
            return """सावधानी बरतें | Continue with caution
सामान्य निगरानी जारी रखें | Maintain regular monitoring"""
    
    def get_active_alerts(self):
        """Get all active alerts"""
        # Clean up old alerts first
        self.cleanup_old_alerts()
        return self.active_alerts
    
    def acknowledge_alert(self, alert_id, acknowledged_by):
        """Acknowledge an alert"""
        for alert in self.active_alerts:
            if alert['id'] == alert_id:
                alert['status'] = 'ACKNOWLEDGED'
                alert['acknowledged_by'] = acknowledged_by
                alert['acknowledged_at'] = datetime.now().isoformat()
                return True
        return False
    
    def resolve_alert(self, alert_id, resolved_by, resolution_notes=''):
        """Resolve an alert"""
        for alert in self.active_alerts:
            if alert['id'] == alert_id:
                alert['status'] = 'RESOLVED'
                alert['resolved_by'] = resolved_by
                alert['resolved_at'] = datetime.now().isoformat()
                alert['resolution_notes'] = resolution_notes
                return True
        return False
    
    def cleanup_old_alerts(self):
        """Remove alerts older than 24 hours"""
        cutoff_time = datetime.now() - timedelta(hours=24)
        self.active_alerts = [
            alert for alert in self.active_alerts
            if datetime.fromisoformat(alert['timestamp']) > cutoff_time
        ]
    
    def get_alert_statistics(self):
        """Get alert statistics"""
        total_alerts = len(self.active_alerts)
        high_alerts = len([a for a in self.active_alerts if a['alert_level'] == 'HIGH'])
        medium_alerts = len([a for a in self.active_alerts if a['alert_level'] == 'MEDIUM'])
        acknowledged = len([a for a in self.active_alerts if a['status'] == 'ACKNOWLEDGED'])
        resolved = len([a for a in self.active_alerts if a['status'] == 'RESOLVED'])
        
        return {
            'total_alerts': total_alerts,
            'high_risk_alerts': high_alerts,
            'medium_risk_alerts': medium_alerts,
            'acknowledged_alerts': acknowledged,
            'resolved_alerts': resolved,
            'active_alerts': total_alerts - resolved
        }
    
    def _send_individual_sms(self, phone_number, message_body):
        """Send SMS to individual phone number (helper method)"""
        try:
            if Client is None:
                return {'success': False, 'error': 'Twilio not installed'}
                
            if not self.twilio_sid or not self.twilio_token:
                return {'success': False, 'error': 'SMS not configured'}
            
            client = Client(self.twilio_sid, self.twilio_token)
            
            message = client.messages.create(
                body=message_body,
                from_=self.twilio_phone,
                to=phone_number
            )
            
            return {'success': True, 'message_sid': message.sid}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
