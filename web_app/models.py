#!/usr/bin/env python3
"""
Database models for AI-Based Rockfall Prediction System
User authentication and role management system
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication system"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='operator')
    
    # Account status and metadata
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(45))  # IPv6 compatible
    
    # Organization and contact info
    organization = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    position = db.Column(db.String(50))
    
    # Relationships
    mine_access = db.relationship('UserMineAccess', foreign_keys='UserMineAccess.user_id', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    login_attempts = db.relationship('LoginAttempt', foreign_keys='LoginAttempt.user_id', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Set user password with secure hashing"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches stored hash"""
        return check_password_hash(self.password_hash, password)
    
    def get_accessible_mines(self):
        """Get list of mine IDs user can access"""
        if self.role in ['admin', 'emergency']:
            # Admin and emergency users can access all mines
            return 'all'
        
        access_list = self.mine_access.all()
        return [access.mine_id for access in access_list]
    
    def can_access_mine(self, mine_id):
        """Check if user can access specific mine"""
        if self.role in ['admin', 'emergency']:
            return True
        
        accessible_mines = self.get_accessible_mines()
        return mine_id in accessible_mines if accessible_mines != 'all' else True
    
    def get_role_display(self):
        """Get human-readable role name"""
        role_names = {
            'admin': 'System Administrator',
            'supervisor': 'Mining Supervisor',
            'operator': 'Mine Operator',
            'emergency': 'Emergency Response'
        }
        return role_names.get(self.role, 'Unknown Role')
    
    def get_permissions(self):
        """Get user permissions based on role"""
        permissions = {
            'admin': [
                'view_dashboard', 'view_alerts', 'acknowledge_alerts',
                'manage_users', 'manage_mines', 'system_config',
                'emergency_override', 'view_all_data'
            ],
            'supervisor': [
                'view_dashboard', 'view_alerts', 'acknowledge_alerts',
                'manage_team', 'emergency_response', 'view_reports'
            ],
            'operator': [
                'view_dashboard', 'view_alerts', 'view_assigned_mines'
            ],
            'emergency': [
                'view_dashboard', 'view_alerts', 'emergency_override',
                'emergency_response', 'view_all_data'
            ]
        }
        return permissions.get(self.role, [])
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'role_display': self.get_role_display(),
            'organization': self.organization,
            'phone': self.phone,
            'position': self.position,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'accessible_mines': self.get_accessible_mines(),
            'permissions': self.get_permissions()
        }
    
    def __repr__(self):
        return f'<User {self.username}>'

class UserMineAccess(db.Model):
    """User mine access permissions"""
    __tablename__ = 'user_mine_access'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mine_id = db.Column(db.String(20), nullable=False)  # mine_001, mine_002, etc.
    permission_level = db.Column(db.String(20), default='read')  # read, write, admin
    granted_at = db.Column(db.DateTime, default=datetime.utcnow)
    granted_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<UserMineAccess user_id={self.user_id} mine_id={self.mine_id}>'

class LoginAttempt(db.Model):
    """Track login attempts for security"""
    __tablename__ = 'login_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    username = db.Column(db.String(80), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    user_agent = db.Column(db.String(500))
    success = db.Column(db.Boolean, nullable=False)
    failure_reason = db.Column(db.String(100))
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @classmethod
    def get_recent_failed_attempts(cls, username, minutes=30):
        """Get recent failed login attempts"""
        since = datetime.utcnow() - timedelta(minutes=minutes)
        return cls.query.filter(
            cls.username == username,
            cls.success == False,
            cls.attempted_at >= since
        ).count()
    
    @classmethod
    def is_account_locked(cls, username, max_attempts=5, lockout_minutes=30):
        """Check if account is locked due to failed attempts"""
        failed_attempts = cls.get_recent_failed_attempts(username, lockout_minutes)
        return failed_attempts >= max_attempts
    
    def __repr__(self):
        return f'<LoginAttempt {self.username} success={self.success}>'

class UserSession(db.Model):
    """Track user sessions"""
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_token = db.Column(db.String(100), unique=True, nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    def __init__(self, user_id, ip_address=None, user_agent=None, hours=24):
        self.user_id = user_id
        self.session_token = secrets.token_urlsafe(32)
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.expires_at = datetime.utcnow() + timedelta(hours=hours)
    
    def is_expired(self):
        """Check if session is expired"""
        return datetime.utcnow() > self.expires_at
    
    def extend_session(self, hours=24):
        """Extend session expiration time"""
        self.expires_at = datetime.utcnow() + timedelta(hours=hours)
    
    @classmethod
    def cleanup_expired_sessions(cls):
        """Remove expired sessions from database"""
        expired_sessions = cls.query.filter(cls.expires_at < datetime.utcnow()).all()
        for session in expired_sessions:
            db.session.delete(session)
        db.session.commit()
        return len(expired_sessions)
    
    def __repr__(self):
        return f'<UserSession user_id={self.user_id} expires_at={self.expires_at}>'

def create_demo_accounts():
    """Create demo accounts for different roles"""
    demo_users = [
        {
            'username': 'admin_demo',
            'email': 'admin@rockfall.system',
            'password': 'Admin@2024',
            'full_name': 'System Administrator',
            'role': 'admin',
            'organization': 'Mining Safety Authority',
            'position': 'System Administrator',
            'phone': '+91-9876543210'
        },
        {
            'username': 'supervisor_demo',
            'email': 'supervisor@rockfall.system',
            'password': 'Super@2024',
            'full_name': 'Mining Supervisor',
            'role': 'supervisor',
            'organization': 'Jharkhand Mining Corp',
            'position': 'Senior Mining Supervisor',
            'phone': '+91-9876543211'
        },
        {
            'username': 'operator_demo',
            'email': 'operator@rockfall.system',
            'password': 'Oper@2024',
            'full_name': 'Mine Operator',
            'role': 'operator',
            'organization': 'Coal India Limited',
            'position': 'Mining Operator',
            'phone': '+91-9876543212'
        },
        {
            'username': 'emergency_demo',
            'email': 'emergency@rockfall.system',
            'password': 'Emerg@2024',
            'full_name': 'Emergency Response Officer',
            'role': 'emergency',
            'organization': 'Emergency Response Team',
            'position': 'Emergency Response Coordinator',
            'phone': '+91-9876543213'
        }
    ]
    
    created_users = []
    
    for user_data in demo_users:
        # Check if user already exists
        existing_user = User.query.filter_by(username=user_data['username']).first()
        if not existing_user:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                full_name=user_data['full_name'],
                role=user_data['role'],
                organization=user_data['organization'],
                position=user_data['position'],
                phone=user_data['phone'],
                is_active=True,
                email_verified=True
            )
            user.set_password(user_data['password'])
            
            db.session.add(user)
            created_users.append(user_data)
    
    # Add mine access for supervisor and operator
    db.session.commit()
    
    # Assign specific mines to supervisor and operator
    supervisor = User.query.filter_by(username='supervisor_demo').first()
    operator = User.query.filter_by(username='operator_demo').first()
    
    if supervisor:
        # Supervisor can access Jharkhand mines
        supervisor_mines = ['mine_001', 'mine_002', 'mine_003']
        for mine_id in supervisor_mines:
            access = UserMineAccess(user_id=supervisor.id, mine_id=mine_id, permission_level='write')
            db.session.add(access)
    
    if operator:
        # Operator can access only one mine
        access = UserMineAccess(user_id=operator.id, mine_id='mine_001', permission_level='read')
        db.session.add(access)
    
    db.session.commit()
    return created_users

def init_db(app):
    """Initialize database with app context"""
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create demo accounts
        demo_users = create_demo_accounts()
        
        # Clean up old sessions
        UserSession.cleanup_expired_sessions()
        
        return demo_users
