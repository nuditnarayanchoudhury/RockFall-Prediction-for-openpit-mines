#!/usr/bin/env python3
"""
Forms for AI-Based Rockfall Prediction System
Login, signup, and user management forms
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
from models import User
import re

class LoginForm(FlaskForm):
    """User login form"""
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ], render_kw={
        'placeholder': 'Enter your username',
        'class': 'form-control form-control-lg',
        'autocomplete': 'username'
    })
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ], render_kw={
        'placeholder': 'Enter your password',
        'class': 'form-control form-control-lg',
        'autocomplete': 'current-password'
    })
    
    remember_me = BooleanField('Remember Me', render_kw={
        'class': 'form-check-input'
    })

class SignupForm(FlaskForm):
    """User registration form"""
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters'),
        Regexp(
            r'^[a-zA-Z0-9_]+$',
            message='Username can only contain letters, numbers, and underscores'
        )
    ], render_kw={
        'placeholder': 'Choose a unique username',
        'class': 'form-control form-control-lg',
        'autocomplete': 'username'
    })
    
    email = StringField('Email Address', validators=[
        DataRequired(message='Email address is required'),
        Email(message='Please enter a valid email address'),
        Length(max=120, message='Email address is too long')
    ], render_kw={
        'placeholder': 'Enter your email address',
        'class': 'form-control form-control-lg',
        'type': 'email',
        'autocomplete': 'email'
    })
    
    full_name = StringField('Full Name', validators=[
        DataRequired(message='Full name is required'),
        Length(min=2, max=100, message='Full name must be between 2 and 100 characters')
    ], render_kw={
        'placeholder': 'Enter your full name',
        'class': 'form-control form-control-lg',
        'autocomplete': 'name'
    })
    
    organization = StringField('Organization', validators=[
        Length(max=100, message='Organization name is too long')
    ], render_kw={
        'placeholder': 'Enter your organization (optional)',
        'class': 'form-control form-control-lg',
        'autocomplete': 'organization'
    })
    
    position = StringField('Position/Title', validators=[
        Length(max=50, message='Position is too long')
    ], render_kw={
        'placeholder': 'Enter your job title (optional)',
        'class': 'form-control form-control-lg',
        'autocomplete': 'organization-title'
    })
    
    phone = StringField('Phone Number', validators=[
        Length(max=20, message='Phone number is too long'),
        Regexp(
            r'^\+?[\d\s\-\(\)]{10,20}$',
            message='Please enter a valid phone number'
        )
    ], render_kw={
        'placeholder': 'Enter your phone number (optional)',
        'class': 'form-control form-control-lg',
        'type': 'tel',
        'autocomplete': 'tel'
    })
    
    role = SelectField('Role', choices=[
        ('operator', '🟢 Mine Operator - View assigned mines and alerts'),
        ('supervisor', '🟡 Mining Supervisor - Manage team and multiple mines'),
        ('emergency', '🔴 Emergency Response - Emergency override capabilities')
    ], default='operator', validators=[
        DataRequired(message='Please select a role')
    ], render_kw={
        'class': 'form-select form-select-lg'
    })
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, max=128, message='Password must be between 8 and 128 characters'),
        Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]',
            message='Password must contain uppercase, lowercase, number, and special character'
        )
    ], render_kw={
        'placeholder': 'Create a strong password',
        'class': 'form-control form-control-lg',
        'autocomplete': 'new-password'
    })
    
    password_confirm = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ], render_kw={
        'placeholder': 'Confirm your password',
        'class': 'form-control form-control-lg',
        'autocomplete': 'new-password'
    })
    
    terms_accepted = BooleanField('Terms & Conditions', validators=[
        DataRequired(message='You must accept the terms and conditions')
    ], render_kw={
        'class': 'form-check-input'
    })
    
    def validate_username(self, username):
        """Custom validator for username uniqueness"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Username already taken. Please choose a different username.'
            )
    
    def validate_email(self, email):
        """Custom validator for email uniqueness"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'Email address already registered. Please use a different email or try logging in.'
            )
    
    def validate_phone(self, phone):
        """Custom validator for phone number format"""
        if phone.data:
            # Remove spaces, dashes, parentheses for validation
            cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone.data)
            if not re.match(r'^\+?[\d]{10,15}$', cleaned_phone):
                raise ValidationError('Please enter a valid phone number')

class ForgotPasswordForm(FlaskForm):
    """Password reset request form"""
    email = StringField('Email Address', validators=[
        DataRequired(message='Email address is required'),
        Email(message='Please enter a valid email address')
    ], render_kw={
        'placeholder': 'Enter your registered email address',
        'class': 'form-control form-control-lg',
        'type': 'email',
        'autocomplete': 'email'
    })

class ResetPasswordForm(FlaskForm):
    """Password reset form"""
    password = PasswordField('New Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, max=128, message='Password must be between 8 and 128 characters'),
        Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]',
            message='Password must contain uppercase, lowercase, number, and special character'
        )
    ], render_kw={
        'placeholder': 'Enter your new password',
        'class': 'form-control form-control-lg',
        'autocomplete': 'new-password'
    })
    
    password_confirm = PasswordField('Confirm New Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ], render_kw={
        'placeholder': 'Confirm your new password',
        'class': 'form-control form-control-lg',
        'autocomplete': 'new-password'
    })

class ProfileUpdateForm(FlaskForm):
    """User profile update form"""
    full_name = StringField('Full Name', validators=[
        DataRequired(message='Full name is required'),
        Length(min=2, max=100, message='Full name must be between 2 and 100 characters')
    ], render_kw={
        'class': 'form-control',
        'autocomplete': 'name'
    })
    
    email = StringField('Email Address', validators=[
        DataRequired(message='Email address is required'),
        Email(message='Please enter a valid email address'),
        Length(max=120, message='Email address is too long')
    ], render_kw={
        'class': 'form-control',
        'type': 'email',
        'autocomplete': 'email'
    })
    
    organization = StringField('Organization', validators=[
        Length(max=100, message='Organization name is too long')
    ], render_kw={
        'class': 'form-control',
        'autocomplete': 'organization'
    })
    
    position = StringField('Position/Title', validators=[
        Length(max=50, message='Position is too long')
    ], render_kw={
        'class': 'form-control',
        'autocomplete': 'organization-title'
    })
    
    phone = StringField('Phone Number', validators=[
        Length(max=20, message='Phone number is too long')
    ], render_kw={
        'class': 'form-control',
        'type': 'tel',
        'autocomplete': 'tel'
    })

class ChangePasswordForm(FlaskForm):
    """Change password form"""
    current_password = PasswordField('Current Password', validators=[
        DataRequired(message='Current password is required')
    ], render_kw={
        'placeholder': 'Enter your current password',
        'class': 'form-control',
        'autocomplete': 'current-password'
    })
    
    new_password = PasswordField('New Password', validators=[
        DataRequired(message='New password is required'),
        Length(min=8, max=128, message='Password must be between 8 and 128 characters'),
        Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]',
            message='Password must contain uppercase, lowercase, number, and special character'
        )
    ], render_kw={
        'placeholder': 'Enter your new password',
        'class': 'form-control',
        'autocomplete': 'new-password'
    })
    
    new_password_confirm = PasswordField('Confirm New Password', validators=[
        DataRequired(message='Please confirm your new password'),
        EqualTo('new_password', message='Passwords must match')
    ], render_kw={
        'placeholder': 'Confirm your new password',
        'class': 'form-control',
        'autocomplete': 'new-password'
    })

def validate_password_strength(password):
    """
    Validate password strength and return strength score and feedback
    Returns: (score, feedback_messages)
    """
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("At least 8 characters")
    
    if len(password) >= 12:
        score += 1
        
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("At least one lowercase letter")
        
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("At least one uppercase letter")
        
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("At least one number")
        
    if re.search(r'[@$!%*?&]', password):
        score += 1
    else:
        feedback.append("At least one special character (@$!%*?&)")
    
    return score, feedback

def get_password_strength_text(score):
    """Get password strength description"""
    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Fair"
    elif score <= 5:
        return "Good"
    else:
        return "Strong"

def get_password_strength_color(score):
    """Get password strength color class"""
    if score <= 2:
        return "text-danger"
    elif score <= 4:
        return "text-warning"
    elif score <= 5:
        return "text-info"
    else:
        return "text-success"
