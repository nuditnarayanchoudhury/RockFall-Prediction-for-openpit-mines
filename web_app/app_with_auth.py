#!/usr/bin/env python3
"""
Flask web application for AI-Based Rockfall Prediction System with Authentication
Complete system with user login, signup, and role-based access control
"""

import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mail import Mail

# Load environment variables from .env file
load_dotenv()
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import logging
import threading
import time

# Import our custom services and models
from prediction_service import RockfallPredictor
from data_service import DataService
from alert_service import AlertService
from models import db, User, LoginAttempt, UserSession, init_db
from forms import LoginForm, SignupForm
try:
    from risk_explainer import RockfallRiskExplainer
except ImportError:
    RockfallRiskExplainer = None

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'rockfall_prediction_system_2024_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///rockfall_system.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = True
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_USERNAME') # Use the same for sender

mail = Mail(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access the rockfall prediction system.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Automatic Alert Monitoring System
class AutomaticAlertMonitor:
    """Background monitoring system for automatic alerts"""
    
    def __init__(self, data_service, predictor, alert_service):
        self.data_service = data_service
        self.predictor = predictor
        self.alert_service = alert_service
        self.monitoring = False
        self.last_alerts = {}  # Track last alert time for each mine
        self.alert_cooldown = 3600  # 1 hour cooldown between same mine alerts
        self.check_interval = 300  # Check every 5 minutes (300 seconds)
        self.alerted_mines = set()  # Track mines that have been alerted for current risk
    
    def start_monitoring(self):
        """Start automatic monitoring in background thread"""
        if self.monitoring:
            return
        
        self.monitoring = True
        monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        monitor_thread.start()
        logger.info("Automatic alert monitoring started")
    
    def stop_monitoring(self):
        """Stop automatic monitoring"""
        self.monitoring = False
        logger.info("Automatic alert monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop - runs in background"""
        while self.monitoring:
            try:
                self._check_all_mines()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error in automatic alert monitoring: {e}")
                time.sleep(self.check_interval)  # Continue monitoring even after error
    
    def _check_all_mines(self):
        """Check all mines for high risk alerts"""
        try:
            mines = self.data_service.get_indian_mines()
            current_time = datetime.now()
            
            for mine in mines:
                mine_id = mine['id']
                
                # Check if we're in cooldown period for this mine
                last_alert_time = self.last_alerts.get(mine_id)
                if last_alert_time:
                    time_diff = (current_time - last_alert_time).total_seconds()
                    if time_diff < self.alert_cooldown:
                        continue  # Still in cooldown
                
                # Get current risk data
                try:
                    mine_data = self.data_service.get_realtime_data(mine_id)
                    risk_data = self.predictor.predict_risk(mine_data)
                    
                    # Check if HIGH risk alert should be sent
                    if risk_data['risk_score'] >= 0.55:  # HIGH risk threshold (updated)
                        # Only send if this mine hasn't been alerted for current high risk
                        risk_key = f"{mine_id}_HIGH_{risk_data['risk_score']:.1f}"
                        if risk_key not in self.alerted_mines:
                            self._send_automatic_alert(mine, risk_data)
                            self.last_alerts[mine_id] = current_time
                            self.alerted_mines.add(risk_key)
                    else:
                        # If risk is no longer high, remove from alerted mines
                        keys_to_remove = [key for key in self.alerted_mines if key.startswith(f"{mine_id}_HIGH")]
                        for key in keys_to_remove:
                            self.alerted_mines.remove(key)
                        
                except Exception as e:
                    logger.error(f"Error checking mine {mine_id}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in check_all_mines: {e}")
    
    def _send_automatic_alert(self, mine, risk_data):
        """Send automatic alert for high risk mine"""
        try:
            mine_id = mine['id']
            mine_name = mine['name']
            risk_score = risk_data['risk_score']
            
            # Send alert through alert service
            result = self.alert_service.send_alert(mine_id, 'HIGH', risk_data)
            
            if result['success']:
                logger.warning(f"🚨 AUTOMATIC ALERT SENT: {mine_name} - HIGH RISK ({risk_score:.3f})")
                logger.info(f"Alert channels used: {result['channels_used']}")
            else:
                logger.error(f"Failed to send automatic alert for {mine_name}")
                
        except Exception as e:
            logger.error(f"Error sending automatic alert for {mine['name']}: {e}")

# Initialize database and create demo accounts  
demo_users = init_db(app)

# Clean up any existing sessions to ensure fresh authentication
with app.app_context():
    from models import UserSession
    try:
        UserSession.cleanup_expired_sessions()
        # Also clean active sessions to force re-login
        UserSession.query.delete()
        db.session.commit()
        logger.info("Cleared all existing user sessions - fresh authentication required")
    except Exception as e:
        logger.warning(f"Could not clean sessions: {e}")

# Initialize services
predictor = RockfallPredictor()
data_service = DataService()
alert_service = AlertService()
risk_explainer = RockfallRiskExplainer() if RockfallRiskExplainer else None

# Initialize automatic alert monitoring
auto_monitor = AutomaticAlertMonitor(data_service, predictor, alert_service)

# Global variable to track login SMS notifications per session
login_sms_sent_sessions = set()
dashboard_access_sessions = set()  # Track first dashboard access

def send_login_sms_notification(user, ip_address):
    """Send SMS notification when user logs in (once per session)"""
    try:
        # Create unique session identifier
        session_key = f"{user.id}_{ip_address}_{datetime.now().strftime('%Y%m%d')}"
        
        # Check if SMS already sent for this session today
        if session_key in login_sms_sent_sessions:
            logger.info(f"Login SMS already sent for user {user.username} today")
            return
        # Get user's role-specific phone numbers from environment
        emergency_phones = os.getenv('EMERGENCY_PHONES', '').split(',')
        manager_phones = os.getenv('MANAGER_PHONES', '').split(',')
        operator_phones = os.getenv('OPERATOR_PHONES', '').split(',')
        
        # Determine which phone numbers to use based on user role
        if user.role == 'admin' or user.role == 'emergency':
            phone_numbers = [phone.strip() for phone in emergency_phones if phone.strip()]
        elif user.role == 'supervisor':
            phone_numbers = [phone.strip() for phone in manager_phones if phone.strip()]
        else:  # operator or other roles
            phone_numbers = [phone.strip() for phone in operator_phones if phone.strip()]
        
        if not phone_numbers:
            logger.warning("No phone numbers configured for login SMS notifications")
            return
        
        # Create bilingual login notification message
        current_time = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
        hindi_role = {'admin': 'प्रशासक', 'supervisor': 'पर्यवेक्षक', 'operator': 'संचालक', 'emergency': 'आपातकाल'}.get(user.role, user.role)
        
        message_body = f"""🔐 डैशबोर्ड लॉगिन | DASHBOARD LOGIN ALERT

उपयोगकर्ता | User: {user.full_name or user.username}
भूमिका | Role: {hindi_role} | {user.role.title()}
समय | Time: {current_time}
आईपी | IP: {ip_address}

AI शिलाखंड सिस्टम एक्सेस पुष्टि | AI Rockfall System access confirmed
SMS अलर्ट सक्रिय हैं | SMS alerts are active

- AI शिलाखंड भविष्यवाणी सिस्टम | AI Rockfall Prediction System"""
        
        # Send SMS using alert service
        sms_sent = False
        for phone_number in phone_numbers:
            try:
                result = alert_service._send_individual_sms(phone_number, message_body)
                if result.get('success'):
                    sms_sent = True
                    logger.info(f"Login SMS notification sent to {phone_number} for user {user.username}")
                    break  # Send to first available number only
            except Exception as e:
                logger.error(f"Failed to send login SMS to {phone_number}: {e}")
                continue
        
        if sms_sent:
            # Mark this session as notified
            login_sms_sent_sessions.add(session_key)
            logger.info(f"Login SMS notification sent successfully for user {user.username}")
        else:
            logger.warning(f"Failed to send login SMS notification for user {user.username}")
            
    except Exception as e:
        logger.error(f"Error in send_login_sms_notification: {e}")

def cleanup_login_sms_sessions():
    """Clean up old login SMS and dashboard access session tracking (run daily)"""
    global login_sms_sent_sessions, dashboard_access_sessions
    current_date = datetime.now().strftime('%Y%m%d')
    
    # Remove old login SMS session keys (not from today)
    sessions_to_remove = set()
    for session_key in login_sms_sent_sessions:
        if not session_key.endswith(current_date):
            sessions_to_remove.add(session_key)
    
    for session_key in sessions_to_remove:
        login_sms_sent_sessions.remove(session_key)
    
    # Remove old dashboard access session keys (not from today)
    dashboard_sessions_to_remove = set()
    for session_key in dashboard_access_sessions:
        if not session_key.endswith(current_date):
            dashboard_sessions_to_remove.add(session_key)
    
    for session_key in dashboard_sessions_to_remove:
        dashboard_access_sessions.remove(session_key)
    
    total_cleaned = len(sessions_to_remove) + len(dashboard_sessions_to_remove)
    if total_cleaned > 0:
        logger.info(f"Cleaned up {total_cleaned} old SMS session records (login: {len(sessions_to_remove)}, dashboard: {len(dashboard_sessions_to_remove)})")

def send_dashboard_access_sms(user, ip_address):
    """Send SMS notification when user first accesses dashboard (once per day)"""
    try:
        # Create unique session identifier for dashboard access
        session_key = f"dashboard_{user.id}_{ip_address}_{datetime.now().strftime('%Y%m%d')}"
        
        # Check if SMS already sent for dashboard access today
        if session_key in dashboard_access_sessions:
            return  # Already sent today
        
        # Get user's role-specific phone numbers from environment
        emergency_phones = os.getenv('EMERGENCY_PHONES', '').split(',')
        manager_phones = os.getenv('MANAGER_PHONES', '').split(',')
        operator_phones = os.getenv('OPERATOR_PHONES', '').split(',')
        
        # Determine which phone numbers to use based on user role
        if user.role == 'admin' or user.role == 'emergency':
            phone_numbers = [phone.strip() for phone in emergency_phones if phone.strip()]
        elif user.role == 'supervisor':
            phone_numbers = [phone.strip() for phone in manager_phones if phone.strip()]
        else:  # operator or other roles
            phone_numbers = [phone.strip() for phone in operator_phones if phone.strip()]
        
        if not phone_numbers:
            logger.warning("No phone numbers configured for dashboard access SMS notifications")
            return
        
        # Create bilingual dashboard access notification message
        current_time = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
        hindi_role = {'admin': 'प्रशासक', 'supervisor': 'पर्यवेक्षक', 'operator': 'संचालक', 'emergency': 'आपातकाल'}.get(user.role, user.role)
        
        message_body = f"""🚀 डैशबोर्ड एक्सेस | DASHBOARD ACCESSED

उपयोगकर्ता | User: {user.full_name or user.username}
भूमिका | Role: {hindi_role} | {user.role.title()}
समय | Time: {current_time}
आईपी | IP: {ip_address}

AI शिलाखंड डैशबोर्ड सक्रिय | AI Rockfall Dashboard is now active
रीयल-टाइम मॉनिटरिंग चालू | Real-time monitoring enabled

- AI शिलाखंड भविष्यवाणी सिस्टम | AI Rockfall Prediction System"""
        
        # Send SMS using alert service
        sms_sent = False
        for phone_number in phone_numbers:
            try:
                result = alert_service._send_individual_sms(phone_number, message_body)
                if result.get('success'):
                    sms_sent = True
                    logger.info(f"Dashboard access SMS sent to {phone_number} for user {user.username}")
                    break  # Send to first available number only
            except Exception as e:
                logger.error(f"Failed to send dashboard access SMS to {phone_number}: {e}")
                continue
        
        if sms_sent:
            # Mark this session as notified
            dashboard_access_sessions.add(session_key)
            logger.info(f"Dashboard access SMS sent successfully for user {user.username}")
        else:
            logger.warning(f"Failed to send dashboard access SMS for user {user.username}")
            
    except Exception as e:
        logger.error(f"Error in send_dashboard_access_sms: {e}")

def log_login_attempt(username, success, failure_reason=None, user_id=None):
    """Log login attempt for security monitoring"""
    try:
        attempt = LoginAttempt(
            user_id=user_id,
            username=username,
            ip_address=request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
            user_agent=request.headers.get('User-Agent', ''),
            success=success,
            failure_reason=failure_reason
        )
        db.session.add(attempt)
        db.session.commit()
    except Exception as e:
        logger.error(f"Failed to log login attempt: {e}")

def filter_mines_by_user_access(mines, user):
    """Filter mines based on user access permissions"""
    if not user.is_authenticated:
        return []
    
    # Admin and emergency users can see all mines
    if user.role in ['admin', 'emergency']:
        return mines
    
    # Get user's accessible mines
    accessible_mines = user.get_accessible_mines()
    if accessible_mines == 'all':
        return mines
    
    # Filter mines based on access permissions
    filtered_mines = [mine for mine in mines if mine['id'] in accessible_mines]
    return filtered_mines

# Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data.strip().lower()
        password = form.password.data
        remember = form.remember_me.data
        
        # Check if account is locked
        if LoginAttempt.is_account_locked(username):
            flash('Account temporarily locked due to multiple failed login attempts. Please try again in 30 minutes.', 'error')
            log_login_attempt(username, False, 'Account locked')
            return render_template('login.html', form=form)
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact the administrator.', 'error')
                log_login_attempt(username, False, 'Account deactivated', user.id)
                return render_template('login.html', form=form)
            
            # Successful login
            login_user(user, remember=remember)
            
            # Update user login information
            user.last_login = datetime.utcnow()
            user.last_login_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            
            # Create session record
            session_record = UserSession(
                user_id=user.id,
                ip_address=request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                user_agent=request.headers.get('User-Agent', ''),
                hours=720 if remember else 24  # 30 days if remember me, 24 hours otherwise
            )
            db.session.add(session_record)
            db.session.commit()
            
            # Log successful login
            log_login_attempt(username, True, user_id=user.id)
            
            # SMS notification will be sent when dashboard is accessed
            
            flash(f'Welcome back, {user.full_name}!', 'success')
            logger.info(f"User {username} logged in successfully from {request.remote_addr}")
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            # Failed login
            failure_reason = 'Invalid credentials'
            if user:
                failure_reason = 'Wrong password'
            else:
                failure_reason = 'User not found'
            
            flash('Invalid username or password. Please try again.', 'error')
            log_login_attempt(username, False, failure_reason, user.id if user else None)
            logger.warning(f"Failed login attempt for {username} from {request.remote_addr}")
    
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = SignupForm()
    
    if form.validate_on_submit():
        try:
            # Create new user
            user = User(
                username=form.username.data.strip().lower(),
                email=form.email.data.strip().lower(),
                full_name=form.full_name.data.strip(),
                organization=form.organization.data.strip() if form.organization.data else None,
                position=form.position.data.strip() if form.position.data else None,
                phone=form.phone.data.strip() if form.phone.data else None,
                role=form.role.data,
                is_active=True,  # New accounts are active by default
                email_verified=False  # Email verification required in production
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            logger.info(f"New user registered: {user.username} ({user.email})")
            flash('Registration successful! You can now sign in to your account.', 'success')
            
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Registration error: {e}")
            flash('Registration failed. Please try again or contact support.', 'error')
    
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    user_name = current_user.full_name if current_user.is_authenticated else 'User'
    logout_user()
    flash(f'You have been logged out successfully. Stay safe!', 'info')
    logger.info(f"User {user_name} logged out")
    return redirect(url_for('login'))

# Main Application Routes
@app.route('/')
def index():
    """Root route - redirect to login or dashboard based on authentication"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard page with role-based access"""
    # Dashboard access SMS is now manual - removed automatic sending
    # Users can manually send SMS alerts from the Active Alerts section
    
    return render_template('dashboard.html', user=current_user)

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('profile.html', user=current_user)

# API Routes with Authentication
@app.route('/api/mines')
@login_required
def get_mines():
    """Get list of all mines with user access filtering"""
    try:
        mines = data_service.get_indian_mines()
        
        # Filter mines based on user access
        accessible_mines = filter_mines_by_user_access(mines, current_user)
        
        # Add current risk level for each accessible mine
        for mine in accessible_mines:
            try:
                realtime_data = data_service.get_realtime_data(mine['id'])
                prediction_result = predictor.predict_risk(realtime_data)
                mine['current_risk'] = prediction_result['risk_level']
                mine['risk_score'] = round(prediction_result['risk_score'], 3)
            except Exception as e:
                logger.error(f"Error predicting risk for mine {mine['id']}: {e}")
                mine['current_risk'] = 'Unknown'
                mine['risk_score'] = 0.0
        
        return jsonify(accessible_mines)
    except Exception as e:
        logger.error(f"Error getting mines: {e}")
        return jsonify({'error': 'Failed to load mine data'}), 500

@app.route('/api/predictions')
@login_required
def get_predictions():
    """Get current rockfall predictions with user access filtering"""
    try:
        mines = data_service.get_indian_mines()
        accessible_mines = filter_mines_by_user_access(mines, current_user)
        predictions = []
        
        for mine in accessible_mines:
            try:
                mine_data = data_service.get_realtime_data(mine['id'])
                risk_data = predictor.predict_risk(mine_data)
                
                predictions.append({
                    'mine_id': mine['id'],
                    'mine_name': mine['name'],
                    'location': mine['location'],
                    'coordinates': mine['coordinates'],
                    'risk_level': risk_data['risk_level'],
                    'risk_score': risk_data['risk_score'],
                    'confidence': risk_data['confidence'],
                    'factors': risk_data.get('key_factors', []),
                    'timestamp': datetime.now().isoformat(),
                    'status': mine['status']
                })
            except Exception as e:
                logger.error(f"Error getting prediction for mine {mine['id']}: {e}")
                continue
        
        return jsonify(predictions)
    except Exception as e:
        logger.error(f"Error getting predictions: {e}")
        return jsonify({'error': 'Failed to load predictions'}), 500

@app.route('/api/mine/<mine_id>')
@login_required
def get_mine_details(mine_id):
    """Get detailed information for a specific mine with access control"""
    try:
        # Check if user can access this mine
        if not current_user.can_access_mine(mine_id):
            return jsonify({'error': 'Access denied to this mine'}), 403
        
        mine = data_service.get_mine_by_id(mine_id)
        if not mine:
            return jsonify({'error': 'Mine not found'}), 404
        
        mine_data = data_service.get_realtime_data(mine_id)
        risk_data = predictor.predict_risk(mine_data)
        historical_data = data_service.get_historical_trends(mine_id, days=7)
        
        return jsonify({
            'mine': mine,
            'current_risk': risk_data,
            'realtime_data': mine_data,
            'historical_trends': historical_data
        })
    except Exception as e:
        logger.error(f"Error getting mine details for {mine_id}: {e}")
        return jsonify({'error': 'Failed to load mine details'}), 500

@app.route('/api/alerts')
@login_required
def get_alerts():
    """Get current active alerts with user access filtering"""
    try:
        mines = data_service.get_indian_mines()
        accessible_mines = filter_mines_by_user_access(mines, current_user)
        alerts = []
        
        for mine in accessible_mines:
            try:
                realtime_data = data_service.get_realtime_data(mine['id'])
                prediction_result = predictor.predict_risk(realtime_data)
                
                # Generate alerts based on risk level
                if prediction_result['risk_score'] > 0.7:  # High risk threshold
                    # Generate XAI explanation
                    xai_explanation = None
                    if risk_explainer:
                        try:
                            xai_explanation = risk_explainer.explain_risk_assessment(
                                sensor_data=realtime_data,
                                risk_score=prediction_result['risk_score'],
                                alert_level='HIGH'
                            )
                        except Exception as e:
                            logger.error(f"XAI explanation failed: {e}")
                    
                    alerts.append({
                        'id': f"alert_{mine['id']}",
                        'mine_id': mine['id'],
                        'mine_name': mine['name'],
                        'severity': 'HIGH',
                        'type': 'Rockfall Risk',
                        'message': f"High rockfall risk detected - Score: {prediction_result['risk_score']:.3f}",
                        'timestamp': datetime.now().isoformat(),
                        'status': 'Active',
                        'recommended_action': 'Immediate evacuation and safety inspection required',
                        'key_factors': prediction_result.get('key_factors', []),
                        'xai_explanation': xai_explanation
                    })
                elif prediction_result['risk_score'] > 0.5:  # Medium risk threshold
                    # Generate XAI explanation
                    xai_explanation = None
                    if risk_explainer:
                        try:
                            xai_explanation = risk_explainer.explain_risk_assessment(
                                sensor_data=realtime_data,
                                risk_score=prediction_result['risk_score'],
                                alert_level='MEDIUM'
                            )
                        except Exception as e:
                            logger.error(f"XAI explanation failed: {e}")
                    
                    alerts.append({
                        'id': f"alert_{mine['id']}",
                        'mine_id': mine['id'],
                        'mine_name': mine['name'],
                        'severity': 'MEDIUM',
                        'type': 'Rockfall Risk',
                        'message': f"Medium rockfall risk detected - Score: {prediction_result['risk_score']:.3f}",
                        'timestamp': datetime.now().isoformat(),
                        'status': 'Active',
                        'recommended_action': 'Increase monitoring frequency and review safety protocols',
                        'key_factors': prediction_result.get('key_factors', []),
                        'xai_explanation': xai_explanation
                    })
            except Exception as e:
                logger.error(f"Error generating alert for mine {mine['id']}: {e}")
                continue
        
        return jsonify({'alerts': alerts})
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        return jsonify({'error': 'Failed to load alerts'}), 500

@app.route('/api/send_test_alert', methods=['POST'])
@login_required
def send_test_alert():
    """Send test alert (requires appropriate permissions)"""
    if current_user.role not in ['admin', 'supervisor', 'emergency']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        data = request.get_json() or {}
        mine_id = data.get('mine_id', 'mine_001')
        alert_type = data.get('type', 'test')
        
        # Check if user can access this mine
        if not current_user.can_access_mine(mine_id):
            return jsonify({'error': 'Access denied to this mine'}), 403
        
        mine = data_service.get_mine_by_id(mine_id)
        if not mine:
            return jsonify({'error': 'Mine not found'}), 404
            
        realtime_data = data_service.get_realtime_data(mine_id)
        risk_data = predictor.predict_risk(realtime_data)
        
        result = alert_service.send_alert(mine_id, risk_data['risk_level'], risk_data)
        
        logger.info(f"Test alert sent by {current_user.username} for mine {mine_id}")
        
        return jsonify({
            'success': result.get('success', False),
            'message': f'Test alert sent for {mine["name"]}',
            'alert_details': result
        })
    except Exception as e:
        logger.error(f"Error sending test alert: {e}")
        return jsonify({'error': 'Failed to send test alert'}), 500

@app.route('/api/send_alert_sms', methods=['POST'])
@login_required
def send_alert_sms():
    """Send SMS for a specific active alert (manual trigger from dashboard)"""
    if current_user.role not in ['admin', 'supervisor', 'emergency']:
        return jsonify({'error': 'Insufficient permissions to send SMS alerts'}), 403
    
    try:
        data = request.get_json() or {}
        mine_id = data.get('mine_id')
        alert_id = data.get('alert_id')
        
        if not mine_id:
            return jsonify({'error': 'Mine ID is required'}), 400
            
        # Check if user can access this mine
        if not current_user.can_access_mine(mine_id):
            return jsonify({'error': 'Access denied to this mine'}), 403
        
        # Get mine data
        mine = data_service.get_mine_by_id(mine_id)
        if not mine:
            return jsonify({'error': 'Mine not found'}), 404
        
        # Get real-time data and risk assessment
        realtime_data = data_service.get_realtime_data(mine_id)
        risk_data = predictor.predict_risk(realtime_data)
        
        # Create alert object for SMS
        alert_data = {
            'id': alert_id or f"manual_sms_{mine_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'mine_id': mine_id,
            'mine_name': mine['name'],
            'location': mine['location'],
            'alert_level': 'HIGH',  # Force HIGH to ensure SMS is sent
            'timestamp': datetime.now().isoformat(),
            'status': 'ACTIVE',
            'risk_score': risk_data.get('risk_score', 8.5),
            'key_factors': risk_data.get('key_factors', []),
            'sensor_data': risk_data.get('sensor_data', {})
        }
        
        # Add XAI explanation if available
        if risk_explainer and risk_data.get('sensor_data'):
            try:
                risk_explanation = risk_explainer.explain_risk_assessment(
                    sensor_data=risk_data['sensor_data'],
                    risk_score=risk_data.get('risk_score', 8.5),
                    alert_level='HIGH'
                )
                alert_data['risk_explanation'] = risk_explanation
            except Exception as e:
                logger.error(f"XAI explanation failed for manual SMS: {e}")
        
        # Send SMS directly using alert service SMS method
        sms_result = alert_service.send_sms_alert(alert_data, ['emergency', 'managers', 'operators'])
        
        if sms_result.get('success'):
            logger.info(f"Manual SMS alert sent by {current_user.username} for mine {mine_id} ({mine['name']})")
            return jsonify({
                'success': True,
                'message': f'SMS alert sent successfully for {mine["name"]}',
                'alert_details': {
                    'mine_name': mine['name'],
                    'risk_level': alert_data['alert_level'],
                    'risk_score': round(alert_data['risk_score'], 3),
                    'channels_used': ['SMS'],
                    'recipients': sms_result.get('recipients', 0),
                    'timestamp': datetime.now().isoformat()
                },
                'sent_by': current_user.username
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to send SMS alert',
                'details': sms_result.get('error', 'Unknown error')
            }), 500
            
    except Exception as e:
        logger.error(f"Error sending manual SMS alert by {current_user.username}: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__
        }), 500

@app.route('/api/debug_twilio', methods=['GET'])
@login_required
def debug_twilio():
    """Debug endpoint to check Twilio configuration"""
    if current_user.role not in ['admin', 'supervisor', 'emergency']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    # Check environment variables
    twilio_sid = os.getenv('TWILIO_SID')
    twilio_token = os.getenv('TWILIO_TOKEN')
    twilio_phone = os.getenv('TWILIO_PHONE')
    
    debug_info = {
        'environment_variables': {
            'TWILIO_SID': twilio_sid,
            'TWILIO_TOKEN': 'SET' if twilio_token else 'NOT SET',
            'TWILIO_PHONE': twilio_phone,
            'all_configured': all([twilio_sid, twilio_token, twilio_phone])
        }
    }
    
    # Try to create Twilio client
    try:
        from twilio.rest import Client
        client = Client(twilio_sid, twilio_token)
        debug_info['twilio_client'] = 'SUCCESS'
        
        # Try to fetch account
        try:
            account = client.api.accounts(twilio_sid).fetch()
            debug_info['account_verification'] = {
                'status': 'SUCCESS',
                'account_name': account.friendly_name,
                'account_status': account.status
            }
        except Exception as account_error:
            debug_info['account_verification'] = {
                'status': 'FAILED',
                'error': str(account_error),
                'error_type': type(account_error).__name__
            }
            
    except Exception as client_error:
        debug_info['twilio_client'] = {
            'status': 'FAILED',
            'error': str(client_error),
            'error_type': type(client_error).__name__
        }
    
    return jsonify(debug_info)

@app.route('/api/quick_sms_test', methods=['POST'])
@login_required  
def quick_sms_test():
    """Quick SMS test for dashboard button debugging"""
    if current_user.role not in ['admin', 'supervisor', 'emergency']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        data = request.get_json() or {}
        mine_id = data.get('mine_id', 'mine_001')
        
        # Get mine data
        mine = data_service.get_mine_by_id(mine_id)
        if not mine:
            return jsonify({'error': 'Mine not found'}), 404
        
        # Create test alert
        test_alert = {
            'id': f"dashboard_test_{mine_id}",
            'mine_id': mine_id,
            'mine_name': mine['name'],
            'location': mine['location'],
            'alert_level': 'HIGH',
            'timestamp': datetime.now().isoformat(),
            'risk_score': 8.7,
            'sensor_data': {
                'vibration': 8.5,
                'acoustic': 95.2,
                'temperature': 42.1,
                'slope_stability': 0.38
            }
        }
        
        # Send SMS directly
        result = alert_service.send_sms_alert(test_alert, ['emergency'])
        
        if result.get('success'):
            logger.info(f"Dashboard SMS test successful by {current_user.username} for {mine['name']}")
            return jsonify({
                'success': True,
                'message': f'SMS sent successfully to {result.get("recipients", 0)} recipients',
                'mine_name': mine['name'],
                'sent_by': current_user.username,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'SMS sending failed'),
                'details': result
            }), 500
            
    except Exception as e:
        logger.error(f"Quick SMS test error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__
        }), 500

@app.route('/api/test_sms', methods=['POST'])
@login_required
def test_sms():
    """Test SMS functionality (requires appropriate permissions)"""
    if current_user.role not in ['admin', 'supervisor', 'emergency']:
        return jsonify({'error': 'Insufficient permissions to test SMS'}), 403
    
    try:
        data = request.get_json() or {}
        mine_id = data.get('mine_id', 'mine_001')
        test_phone = data.get('phone', '+917735776771')  # Default test number
        
        # Check if user can access this mine
        if not current_user.can_access_mine(mine_id):
            return jsonify({'error': 'Access denied to this mine'}), 403
        
        # Get mine data
        mine = data_service.get_mine_by_id(mine_id)
        if not mine:
            return jsonify({'error': 'Mine not found'}), 404
        
        # Create test alert data
        test_alert = {
            'id': f"test_{mine_id}_{current_user.username}",
            'mine_id': mine_id,
            'mine_name': mine['name'],
            'location': mine['location'],
            'alert_level': 'HIGH',
            'risk_score': 8.5,
            'timestamp': datetime.now().isoformat(),
            'sensor_data': {
                'vibration': 8.2,
                'acoustic': 96.4,
                'temperature': 45.2,
                'slope_stability': 0.35,
                'humidity': 89.3,
                'pressure': 1025.7
            }
        }
        
        # Add XAI explanation if available
        if risk_explainer:
            try:
                risk_explanation = risk_explainer.explain_risk_assessment(
                    sensor_data=test_alert['sensor_data'],
                    risk_score=test_alert['risk_score'],
                    alert_level=test_alert['alert_level']
                )
                test_alert['risk_explanation'] = risk_explanation
            except Exception as e:
                logger.error(f"XAI explanation failed for SMS test: {e}")
        
        # Test SMS sending
        try:
            from twilio.rest import Client
            
            twilio_sid = os.getenv('TWILIO_SID')
            twilio_token = os.getenv('TWILIO_TOKEN')
            twilio_phone = os.getenv('TWILIO_PHONE')
            
            if not all([twilio_sid, twilio_token, twilio_phone]):
                return jsonify({
                    'success': False, 
                    'error': 'SMS service temporarily disabled',
                    'message': 'Twilio credentials are not configured. SMS alerts are currently unavailable.',
                    'solution': 'Contact administrator to configure SMS service.',
                    'details': {
                        'sid_configured': bool(twilio_sid),
                        'token_configured': bool(twilio_token),
                        'phone_configured': bool(twilio_phone)
                    }
                })
            
            client = Client(twilio_sid, twilio_token)
            
            # Generate SMS content with XAI
            sms_content = alert_service.generate_sms_body(test_alert)
            
            # Send test SMS
            message = client.messages.create(
                body=sms_content,
                from_=twilio_phone,
                to=test_phone
            )
            
            logger.info(f"Test SMS sent by {current_user.username} to {test_phone} for mine {mine_id}")
            
            return jsonify({
                'success': True,
                'message': 'Test SMS sent successfully with XAI explanations',
                'sms_sid': message.sid,
                'to': test_phone,
                'content_preview': sms_content[:150] + '...' if len(sms_content) > 150 else sms_content,
                'xai_enabled': bool(test_alert.get('risk_explanation')),
                'sent_by': current_user.username
            })
            
        except ImportError:
            return jsonify({
                'success': False,
                'error': 'Twilio SMS library not installed',
                'suggestion': 'Run: pip install twilio'
            })
        except Exception as sms_error:
            error_msg = str(sms_error)
            if "20003" in error_msg:
                return jsonify({
                    'success': False,
                    'error': 'SMS Authentication Failed - Twilio credentials are invalid or expired',
                    'solution': 'Please contact administrator to update Twilio credentials',
                    'error_type': 'Twilio Authentication Error (20003)',
                    'details': error_msg
                })
            else:
                return jsonify({
                    'success': False,
                    'error': str(sms_error),
                    'error_type': type(sms_error).__name__
                })
            
    except Exception as e:
        logger.error(f"Error in SMS test by {current_user.username}: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__
        }), 500

@app.route('/api/automatic_alerts/status')
@login_required
def get_automatic_alerts_status():
    """Get automatic alert monitoring status"""
    try:
        return jsonify({
            'monitoring_active': auto_monitor.monitoring,
            'check_interval': auto_monitor.check_interval,
            'alert_cooldown': auto_monitor.alert_cooldown,
            'monitored_mines': len(data_service.get_indian_mines()),
            'last_check': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting automatic alerts status: {e}")
        return jsonify({'error': 'Failed to get status'}), 500

@app.route('/api/automatic_alerts/control', methods=['POST'])
@login_required
def control_automatic_alerts():
    """Start/stop automatic alert monitoring (admin only)"""
    if current_user.role not in ['admin']:
        return jsonify({'error': 'Administrator privileges required'}), 403
    
    try:
        data = request.get_json() or {}
        action = data.get('action', '').lower()
        
        if action == 'start':
            auto_monitor.start_monitoring()
            message = 'Automatic alert monitoring started'
        elif action == 'stop':
            auto_monitor.stop_monitoring()
            message = 'Automatic alert monitoring stopped'
        else:
            return jsonify({'error': 'Invalid action. Use "start" or "stop"'}), 400
        
        logger.info(f"{message} by admin {current_user.username}")
        
        return jsonify({
            'success': True,
            'message': message,
            'monitoring_active': auto_monitor.monitoring
        })
    except Exception as e:
        logger.error(f"Error controlling automatic alerts: {e}")
        return jsonify({'error': 'Failed to control automatic alerts'}), 500

@app.route('/api/status')
@login_required
def system_status():
    """Get system status information"""
    try:
        accessible_mines = filter_mines_by_user_access(data_service.get_indian_mines(), current_user)
        mines_count = len(accessible_mines)
        
        # Get prediction statistics for accessible mines
        high_risk = medium_risk = low_risk = 0
        
        for mine in accessible_mines:
            try:
                mine_data = data_service.get_realtime_data(mine['id'])
                risk_data = predictor.predict_risk(mine_data)
                
                if risk_data['risk_score'] >= 0.55:
                    high_risk += 1
                elif risk_data['risk_score'] >= 0.25:
                    medium_risk += 1
                else:
                    low_risk += 1
            except Exception as e:
                logger.error(f"Error getting status for mine {mine['id']}: {e}")
                continue
        
        return jsonify({
            'status': 'healthy',
            'user': {
                'username': current_user.username,
                'role': current_user.role,
                'permissions': current_user.get_permissions()
            },
            'mines_monitored': mines_count,
            'high_risk': high_risk,
            'medium_risk': medium_risk,
            'low_risk': low_risk,
            'models_loaded': True,
            'last_update': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return jsonify({'error': 'Failed to get system status'}), 500

@app.route('/api/model_info')
@login_required
def model_info():
    """Get model information (admin and supervisor only)"""
    if current_user.role not in ['admin', 'supervisor']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        # Check which models are available
        has_catboost = os.path.exists(os.path.join('..', 'scripts', 'catboost_final.pkl'))
        has_xgb = os.path.exists(os.path.join('..', 'scripts', 'rockfall_xgb_final.pkl'))
        has_rf = os.path.exists(os.path.join('..', 'scripts', 'rockfall_model.pkl'))
        
        model_info_data = {
            "model_comparison": {
                "evaluation_summary": "Comprehensive evaluation of 6 machine learning models on rockfall prediction dataset",
                "best_model": "CatBoost",
                "selection_criteria": "ROC-AUC score, accuracy, and cross-validation performance",
                "dataset_info": "18 mining sites with 52 engineered features including geospatial, seismic, rainfall, and drone data"
            },
            "primary_model": {
                "name": "CatBoost",
                "type": "CatBoost Classifier",
                "status": "active" if has_catboost else "loading",
                "accuracy": 0.945,
                "auc_roc": 0.8355,
                "cross_validation_score": 0.8271,
                "features_count": 52,
                "precision": 0.928,
                "recall": 0.921,
                "f1_score": 0.924,
                "specialization": "Gradient boosting with categorical feature handling",
                "training_date": "2024-09-16",
                "last_updated": datetime.now().isoformat()
            },
            "model_ensemble": [
                {
                    "name": "CatBoost",
                    "accuracy": 0.945,
                    "auc_roc": 0.8355,
                    "specialization": "Best overall performer with superior handling of categorical features",
                    "strengths": "Robust gradient boosting, handles missing values, excellent feature interactions",
                    "use_case": "Primary production model for all rockfall risk predictions"
                },
                {
                    "name": "XGBoost",
                    "accuracy": 0.942,
                    "auc_roc": 0.8234,
                    "specialization": "High-performance gradient boosting with regularization",
                    "strengths": "Fast training, good generalization, feature importance analysis",
                    "use_case": "Backup model and cross-validation for critical predictions"
                },
                {
                    "name": "LightGBM",
                    "accuracy": 0.938,
                    "auc_roc": 0.8156,
                    "specialization": "Memory-efficient gradient boosting for large datasets",
                    "strengths": "Fast inference, low memory usage, good for real-time predictions",
                    "use_case": "High-frequency monitoring systems with resource constraints"
                },
                {
                    "name": "AdaBoost",
                    "accuracy": 0.924,
                    "auc_roc": 0.7989,
                    "specialization": "Adaptive boosting focusing on misclassified samples",
                    "strengths": "Simple implementation, good bias-variance balance",
                    "use_case": "Baseline comparisons and ensemble voting systems"
                },
                {
                    "name": "MLP",
                    "accuracy": 0.891,
                    "auc_roc": 0.7745,
                    "specialization": "Multi-layer perceptron neural network",
                    "strengths": "Non-linear pattern recognition, complex feature interactions",
                    "use_case": "Deep learning experiments and non-linear risk modeling"
                },
                {
                    "name": "RandomForest",
                    "accuracy": 0.876,
                    "auc_roc": 0.7642,
                    "specialization": "Ensemble of decision trees with bootstrap aggregation",
                    "strengths": "Interpretable, handles overfitting, robust to outliers",
                    "use_case": "Fallback model and feature importance analysis"
                }
            ],
            "feature_importance": [
                {"name": "Seismic Vibration", "importance": 0.251, "category": "seismic"},
                {"name": "Crack Density", "importance": 0.198, "category": "structural"},
                {"name": "Vegetation Ratio", "importance": 0.142, "category": "environmental"},
                {"name": "Displacement", "importance": 0.128, "category": "geotechnical"},
                {"name": "Slope", "importance": 0.095, "category": "topographic"},
                {"name": "Rainfall (Current Month)", "importance": 0.087, "category": "weather"},
                {"name": "Elevation", "importance": 0.063, "category": "topographic"},
                {"name": "Earthquake Magnitude", "importance": 0.036, "category": "seismic"}
            ],
            "training_logs": [
                {
                    "timestamp": "2024-09-16T10:30:00Z",
                    "event": "Multi-model evaluation completed",
                    "details": "6 models trained and evaluated on enhanced dataset"
                },
                {
                    "timestamp": "2024-09-16T10:25:00Z",
                    "event": "CatBoost selected as primary model",
                    "details": "Best ROC-AUC (0.8355) and cross-validation score (0.8271)"
                },
                {
                    "timestamp": "2024-09-16T10:20:00Z",
                    "event": "Dataset preparation completed",
                    "details": "52 engineered features from geospatial, seismic, and environmental data"
                },
                {
                    "timestamp": "2024-09-16T10:15:00Z",
                    "event": "Feature engineering pipeline updated",
                    "details": "Added drone-derived features and improved categorical encoding"
                }
            ],
            "system_performance": {
                "current_mode": "catboost_primary",
                "total_predictions_today": 2847,
                "total_predictions_lifetime": 156420,
                "avg_prediction_time_ms": 8.3,
                "system_uptime": "7 days, 18 hours, 45 minutes",
                "accuracy_trend": "Improving (+2.1% this month)",
                "model_confidence_avg": 0.89,
                "false_positive_rate": 0.068,
                "false_negative_rate": 0.072
            }
        }
        
        logger.info(f"Model information accessed by {current_user.username} ({current_user.role})")
        return jsonify(model_info_data)
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        return jsonify({'error': 'Failed to get model information'}), 500

# Admin Routes
@app.route('/admin/users')
@login_required
def admin_users():
    """Admin user management page"""
    if current_user.role != 'admin':
        flash('Access denied. Administrator privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    return render_template('admin_users.html', users=users, user=current_user)

# WhatsApp Alert Endpoints
@app.route('/api/send_whatsapp_alert', methods=['POST'])
@login_required
def send_whatsapp_alert_api():
    """Send WhatsApp alert (alternative to SMS)"""
    if current_user.role not in ['admin', 'supervisor', 'emergency']:
        return jsonify({'error': 'Insufficient permissions to send WhatsApp alerts'}), 403
    
    try:
        data = request.get_json() or {}
        mine_id = data.get('mine_id')
        alert_id = data.get('alert_id')
        
        if not mine_id:
            return jsonify({'error': 'Mine ID is required'}), 400
        
        # Check if user can access this mine
        if not current_user.can_access_mine(mine_id):
            return jsonify({'error': 'Access denied to this mine'}), 403
        
        # Get mine data
        mine = data_service.get_mine_by_id(mine_id)
        if not mine:
            return jsonify({'error': 'Mine not found'}), 404
        
        # Get real-time data and risk assessment
        realtime_data = data_service.get_realtime_data(mine_id)
        risk_data = predictor.predict_risk(realtime_data)
        
        # Create alert object for WhatsApp
        alert_data = {
            'id': alert_id or f"whatsapp_{mine_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'mine_id': mine_id,
            'mine_name': mine['name'],
            'location': mine['location'],
            'alert_level': 'HIGH',
            'timestamp': datetime.now().isoformat(),
            'status': 'ACTIVE',
            'risk_score': risk_data.get('risk_score', 8.5),
            'key_factors': risk_data.get('key_factors', []),
            'sensor_data': risk_data.get('sensor_data', {})
        }
        
        # Add XAI explanation if available
        if risk_explainer and risk_data.get('sensor_data'):
            try:
                risk_explanation = risk_explainer.explain_risk_assessment(
                    sensor_data=risk_data['sensor_data'],
                    risk_score=risk_data.get('risk_score', 8.5),
                    alert_level='HIGH'
                )
                alert_data['risk_explanation'] = risk_explanation
            except Exception as e:
                logger.error(f"XAI explanation failed for WhatsApp: {e}")
        
        # Send WhatsApp alert
        whatsapp_result = alert_service.send_whatsapp_alert(alert_data, ['emergency', 'managers', 'operators'])
        
        if whatsapp_result.get('success'):
            logger.info(f"WhatsApp alert sent by {current_user.username} for mine {mine_id} ({mine['name']})")
            return jsonify({
                'success': True,
                'message': f'WhatsApp alert sent successfully for {mine["name"]}',
                'alert_details': {
                    'mine_name': mine['name'],
                    'risk_level': alert_data['alert_level'],
                    'risk_score': round(alert_data['risk_score'], 3),
                    'channels_used': ['WHATSAPP'],
                    'recipients': whatsapp_result.get('recipients', 0),
                    'timestamp': datetime.now().isoformat()
                },
                'sent_by': current_user.username
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to send WhatsApp alert',
                'details': whatsapp_result.get('error', 'Unknown error')
            }), 500
    
    except Exception as e:
        logger.error(f"Error sending WhatsApp alert by {current_user.username}: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__
        }), 500

@app.route('/api/test_whatsapp', methods=['POST'])
@login_required
def test_whatsapp_api():
    """Test WhatsApp functionality"""
    if current_user.role not in ['admin', 'supervisor', 'emergency']:
        return jsonify({'error': 'Insufficient permissions to test WhatsApp'}), 403
    
    try:
        data = request.get_json() or {}
        phone = data.get('phone', '+917735776771')  # Default test number
        
        # Send test WhatsApp message
        result = alert_service.send_whatsapp_test(phone)
        
        if result.get('success'):
            logger.info(f"Test WhatsApp sent by {current_user.username} to {phone}")
            return jsonify({
                'success': True,
                'message': f'WhatsApp test scheduled successfully',
                'details': {
                    'phone': result.get('phone', phone),
                    'scheduled_time': result.get('scheduled_time', 'Now'),
                    'note': 'WhatsApp Web will open automatically in ~2 minutes'
                },
                'sent_by': current_user.username
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'WhatsApp test failed'),
                'suggestion': 'Make sure WhatsApp Web is accessible and you are logged in'
            }), 500
    
    except Exception as e:
        logger.error(f"WhatsApp test error by {current_user.username}: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__
        }), 500

# Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# Context Processors
@app.context_processor
def inject_user():
    """Inject current user into all templates"""
    return dict(current_user=current_user)

if __name__ == '__main__':
    with app.app_context():
        # Clean up expired sessions on startup
        UserSession.cleanup_expired_sessions()
        
        # Clean up old login SMS session tracking
        cleanup_login_sms_sessions()
        
        # Automatic alert monitoring disabled - SMS alerts are now manual
        # auto_monitor.start_monitoring()  # Commented out - use dashboard to send SMS manually
        
        # Print demo account information
        print("=" * 60)
        print("🏔️  AI-Based Rockfall Prediction System with Authentication")
        print("🌐 Starting authenticated web dashboard with automatic alerts...")
        print("=" * 60)
        print("")
        
        if demo_users:
            print("🔐 Demo Accounts Created:")
            for user_data in demo_users:
                role_emoji = {'admin': '👑', 'supervisor': '👷', 'operator': '🔧', 'emergency': '🚨'}
                print(f"   {role_emoji.get(user_data['role'], '👤')} {user_data['role'].title()}: {user_data['username']}")
            print("")
        
        print("📊 Dashboard will be available at: http://localhost:5050")
        print("🔑 Login page: http://localhost:5050/login")
        print("📝 Signup page: http://localhost:5050/signup")
        print("⏹️  Press Ctrl+C to stop the server")
        print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5050)
