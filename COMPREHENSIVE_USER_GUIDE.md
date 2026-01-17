# 🏔️ AI-Based Rockfall Prediction System - Comprehensive User Guide

## Complete Installation, Configuration, and Usage Manual

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Guide](#installation-guide)
3. [Configuration Setup](#configuration-setup)
4. [User Account Management](#user-account-management)
5. [Using the Dashboard](#using-the-dashboard)
6. [Understanding XAI Explanations](#understanding-xai-explanations)
7. [Alert System Usage](#alert-system-usage)
8. [API Reference](#api-reference)
9. [Troubleshooting](#troubleshooting)
10. [Maintenance Guide](#maintenance-guide)

---

## 💻 System Requirements

### **Minimum Requirements**
- **Operating System**: Windows 10, macOS 10.14, Ubuntu 18.04, or newer
- **Python**: Version 3.8 or higher
- **Memory (RAM)**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space for application, 5GB for datasets
- **Network**: Broadband internet connection for CDN resources
- **Browser**: Chrome 80+, Firefox 75+, Edge 80+, Safari 13+

### **Recommended Specifications**
- **CPU**: Dual-core processor (2.5GHz+) for optimal performance
- **Memory**: 8GB RAM for smooth operation with multiple users
- **Storage**: SSD recommended for faster data processing
- **Network**: High-speed internet for real-time updates and alerts

### **For Production Deployment**
- **Server**: Linux-based server (Ubuntu 20.04 LTS recommended)
- **CPU**: Quad-core processor (3.0GHz+)
- **Memory**: 16GB RAM for concurrent users
- **Storage**: 50GB+ SSD storage
- **Network**: Dedicated internet connection with static IP

---

## 🚀 Installation Guide

### **Step 1: Download and Extract Project**

#### Option A: Download ZIP
1. Download the project ZIP file
2. Extract to your desired location (e.g., `C:\Users\YourName\SIH_PROJECT`)
3. Open terminal/command prompt in the project directory

#### Option B: Clone Repository (if available)
```bash
git clone <repository-url>
cd SIH_PROJECT
```

### **Step 2: Install Python Dependencies**

Navigate to the web application directory:
```bash
cd web_app
```

Install required packages:
```bash
# Install all dependencies
pip install -r requirements.txt

# If you encounter issues, try upgrading pip first:
pip install --upgrade pip
pip install -r requirements.txt
```

### **Step 3: Verify Installation**

Run the system test to ensure everything is working:
```bash
python test_system.py
```

**Expected Output:**
```
=== AI Rockfall Prediction System - Component Test ===
✓ Flask imported successfully
✓ DataService: Loaded 18 Indian mines
✓ PredictionService: ML models loaded
✓ AlertService: Alert generation working
✓ Integration test: All systems operational
=== Test Results ===
Passed: 5, Failed: 0, Total: 5
🎉 All tests passed! System is ready to run.
```

### **Step 4: Run the Application**

Start the application:
```bash
python app_with_auth.py
```

**Expected Output:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment.
```

### **Step 5: Access the Dashboard**

1. Open your web browser
2. Navigate to: `http://localhost:5000`
3. You'll be redirected to the login page
4. Use demo credentials or create a new account

---

## ⚙️ Configuration Setup

### **Environment Variables (Optional)**

Create a `.env` file in the `web_app` directory for custom configuration:

```bash
# Copy the template
cp .env.template .env
```

Edit `.env` with your preferred settings:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here

# Database Configuration (SQLite by default)
DATABASE_URL=sqlite:///rockfall_system.db

# Email Alerts Configuration (Optional)
EMAIL_ENABLED=true
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# SMS Alerts Configuration (Optional - requires Twilio account)
SMS_ENABLED=false
TWILIO_SID=your_twilio_account_sid
TWILIO_TOKEN=your_twilio_auth_token
TWILIO_PHONE=+1234567890

# Risk Thresholds
HIGH_RISK_THRESHOLD=0.7
MEDIUM_RISK_THRESHOLD=0.4
CONFIDENCE_THRESHOLD=0.6

# XAI Configuration
XAI_ENABLED=true
XAI_DETAILED_ANALYSIS=true

# Multilingual Configuration
MULTILINGUAL_ENABLED=true
DEFAULT_LANGUAGES=hindi,english
```

### **Email Setup (Gmail Example)**

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. **Update .env file**:
   ```env
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASSWORD=generated_app_password
   ```

### **SMS Setup (Twilio)**

1. **Create Twilio Account**: Visit twilio.com
2. **Get Credentials**:
   - Account SID
   - Auth Token
   - Phone Number
3. **Update .env file**:
   ```env
   SMS_ENABLED=true
   TWILIO_SID=your_account_sid
   TWILIO_TOKEN=your_auth_token
   TWILIO_PHONE=your_twilio_number
   ```

---

## 👤 User Account Management

### **Default Demo Accounts**

The system comes with pre-configured demo accounts:

| Username | Password | Role | Access Level |
|----------|----------|------|--------------|
| `admin_demo` | `Admin@2024` | Admin | Full system access |
| `supervisor_demo` | `Super@2024` | Supervisor | Mine oversight |
| `operator_demo` | `Oper@2024` | Operator | Basic monitoring |
| `emergency_demo` | `Emerg@2024` | Emergency | Emergency response |

### **Creating New Accounts**

#### Via Web Interface:
1. Go to `http://localhost:5000`
2. Click "Create Account" on login page
3. Fill in the registration form:
   - **Username**: Unique identifier
   - **Email**: Valid email address
   - **Password**: Strong password (8+ characters)
   - **Role**: Select appropriate role
4. Submit and login

#### Role Descriptions:

**Admin Role:**
- Full system configuration access
- User management capabilities
- System monitoring and maintenance
- All mine access permissions

**Supervisor Role:**
- Mine operation oversight
- Alert acknowledgment and resolution
- Team management for assigned mines
- Safety protocol implementation

**Operator Role:**
- Mine-specific monitoring
- Basic alert viewing
- Operational status reporting
- Limited administrative access

**Emergency Role:**
- Emergency response coordination
- All-mines access during emergencies
- Evacuation protocol activation
- Critical incident management

### **Managing User Accounts**

#### Password Reset:
1. Login as Admin
2. Go to User Management section
3. Select user and reset password
4. Provide new temporary password to user

#### Role Changes:
1. Admin users can modify user roles
2. Changes take effect immediately
3. Users may need to re-login

---

## 🌐 Using the Dashboard

### **Login Process**

1. **Access URL**: Navigate to `http://localhost:5000`
2. **Enter Credentials**: Username and password
3. **Select "Remember Me"**: (Optional) For extended sessions
4. **Click Login**: You'll be redirected to the dashboard

### **Dashboard Overview**

The dashboard contains multiple sections:

#### **Navigation Bar**
- **System Status**: Green (Healthy) or Red (Issues)
- **Current Time**: Live clock display
- **User Info**: Logged-in user and role
- **Logout Button**: Secure session termination

#### **Tab Navigation**
- **Overview**: Main monitoring dashboard
- **Alerts**: Active and historical alerts
- **Analytics**: Data analysis and trends
- **Models**: ML model information and performance

### **Overview Tab Features**

#### **Statistics Cards**
- **Total Mines**: 18 Indian mining sites
- **High Risk**: Number of mines with high risk
- **Medium Risk**: Mines with elevated risk
- **Low Risk**: Mines with normal conditions

#### **Interactive Mine Map**
- **Mine Locations**: All 18 mines displayed with GPS coordinates
- **Risk Indicators**: Color-coded markers
  - 🔴 Red: High Risk
  - 🟡 Yellow: Medium Risk  
  - 🟢 Green: Low Risk
- **Click Interaction**: Click any mine marker for details
- **Mine Information Popup**:
  - Mine name and location
  - Current risk level and score
  - Operator and contact information
  - Key risk factors

#### **Risk Trends Chart**
- **7-Day History**: Historical risk level changes
- **Real-Time Updates**: Updates every 30 seconds
- **Interactive**: Hover for specific data points

#### **Weather Widget**
- **Current Conditions**: Temperature and weather
- **Location-Based**: Updates based on selected mine
- **Seasonal Information**: Monsoon and weather patterns

#### **Active Alerts Panel**
- **Recent Alerts**: Latest system alerts
- **Scrollable List**: Navigate through alerts
- **Alert Details**: Risk level, mine, timestamp
- **Quick Actions**: View details or acknowledge

#### **Mine Details Panel**
- **Dynamic Content**: Updates based on map selection
- **Comprehensive Info**: Complete mine information
- **Sensor Data**: Real-time sensor readings
- **XAI Explanations**: Risk factor analysis

### **Alerts Tab Features**

#### **Critical Alerts Section**
- **High-Priority Alerts**: RED alerts requiring immediate attention
- **Emergency Information**: Contact numbers and procedures
- **Action Requirements**: Specific steps for each alert
- **Timeline**: When alerts were triggered

#### **Alert Timeline Chart**
- **Historical View**: Past 24 hours of alert activity
- **Alert Distribution**: By severity and time
- **Trend Analysis**: Alert frequency patterns

#### **Emergency Action Plans**
- **Evacuation Procedures**: Step-by-step guides
- **Emergency Contacts**: Key personnel and services
- **Equipment Protocols**: Machinery shutdown procedures
- **Communication Plans**: Alert routing and escalation

### **Analytics Tab Features**

#### **Risk Distribution Pie Chart**
- **Current Risk Breakdown**: Percentage by risk level
- **Visual Overview**: Easy-to-understand risk summary
- **Real-Time Updates**: Reflects current system state

#### **State-wise Analysis**
- **Horizontal Bar Chart**: Risk levels by Indian state
- **Geographic Insights**: Regional risk patterns
- **Comparative View**: State-by-state comparison

#### **Real-Time Sensor Data**
- **Animated Radar Chart**: Live sensor readings
- **Multiple Parameters**: Vibration, acoustic, temperature, etc.
- **Threshold Indicators**: Visual limit markers
- **Interactive**: Click for detailed information

#### **Monthly Trends**
- **Historical Analysis**: Long-term risk patterns
- **Seasonal Factors**: Weather and monsoon impacts
- **Trend Identification**: Risk pattern recognition

### **Models Tab Features**

#### **Model Information Panel**
- **Primary Model**: XGBoost performance metrics
- **Fallback Model**: Random Forest statistics
- **Accuracy Metrics**: Training and validation scores
- **Model Status**: Current operational state

#### **Feature Importance Chart**
- **Top Contributing Factors**: Most important prediction features
- **Ranked Display**: Features ordered by importance
- **Technical Insights**: Understanding model decisions

#### **Performance Metrics**
- **Accuracy Scores**: Model prediction accuracy
- **Confidence Levels**: Reliability measurements
- **Processing Times**: System response performance
- **Success Rates**: Alert delivery statistics

---

## ✨ Understanding XAI Explanations

### **What is XAI?**

**Explainable AI (XAI)** makes AI decisions transparent and understandable. Instead of just saying "HIGH RISK", our system explains exactly WHY there's high risk and what specific actions to take.

### **XAI Components**

#### **1. Primary Explanation**
Clear, simple explanation of the current risk assessment:
```
"HIGH RISK DETECTED: Critical threshold exceeded for vibration (8.2 vs 7.5). 
Primary risk contributors: vibration (critical), slope_stability (high), acoustic (high)."
```

#### **2. Contributing Factors**
Detailed breakdown of risk factors:
- **Factor Name**: What sensor or condition
- **Current Value**: Actual reading
- **Risk Level**: How dangerous (low/medium/high/critical)
- **Contribution Score**: How much it affects total risk (0-10 scale)

#### **3. Threshold Violations**
Specific safety limits that have been exceeded:
- **Sensor Type**: Which sensor exceeded limits
- **Current Value**: Current reading
- **Threshold Value**: Safety limit
- **Percentage Over**: How much the limit was exceeded

#### **4. AI Recommendations**
Specific actions to take immediately:
- **Priority Order**: Most critical actions first
- **Specific Instructions**: Exactly what to do
- **Equipment Specific**: Which machines to stop
- **Personnel Actions**: Evacuation or safety procedures

#### **5. Confidence Level**
How reliable the assessment is (0-100%):
- **90%+ Confidence**: Very reliable, act immediately
- **70-90% Confidence**: Reliable, take recommended actions
- **50-70% Confidence**: Moderate confidence, increase monitoring
- **<50% Confidence**: Low confidence, use caution

### **Reading XAI Alerts**

#### **High Risk Example:**
```json
{
  "primary_explanation": "HIGH RISK: Critical vibration at 8.2Hz exceeds 7.5Hz threshold",
  "confidence_level": 95.2,
  "contributing_factors": [
    {"factor": "vibration", "value": 8.2, "risk_level": "critical", "score": 10.0},
    {"factor": "acoustic", "value": 96.4, "risk_level": "high", "score": 9.0}
  ],
  "threshold_violations": [
    {"sensor": "vibration", "current": 8.2, "threshold": 7.5, "exceeded_by": "9.3%"}
  ],
  "recommendations": [
    "🚨 IMMEDIATE EVACUATION: Remove all personnel from danger zones",
    "🔍 VIBRATION CHECK: Inspect for structural instability",
    "⛔ EQUIPMENT STOP: Halt all heavy machinery"
  ]
}
```

**How to Read This:**
1. **High confidence (95.2%)** means this is very reliable
2. **Vibration is critical** - this is the main problem
3. **8.2Hz reading exceeds 7.5Hz limit** by 9.3%
4. **Take immediate action** - evacuate and stop equipment

#### **Medium Risk Example:**
```json
{
  "primary_explanation": "MEDIUM RISK: Multiple sensors showing elevated readings",
  "confidence_level": 78.3,
  "contributing_factors": [
    {"factor": "crack_density", "value": 0.032, "risk_level": "high", "score": 7.2},
    {"factor": "rainfall", "value": 185.5, "risk_level": "medium", "score": 6.1}
  ],
  "recommendations": [
    "👥 INCREASE MONITORING: Check sensors every 2 hours",
    "⚠️ RESTRICT ACCESS: Limit personnel in unstable areas"
  ]
}
```

**How to Read This:**
1. **Good confidence (78.3%)** - reasonably reliable
2. **Multiple factors** contributing to risk
3. **No immediate emergency** but increased caution needed
4. **Preventive actions** - increase monitoring and restrict access

### **XAI in Different Languages**

The system provides XAI explanations in local languages:

**English:**
"Critical vibration detected: 8.2Hz exceeds 7.5Hz safety threshold"

**Hindi:**  
"गंभीर कंपन: 8.2Hz सुरक्षा सीमा 7.5Hz से अधिक"

**Bengali:**
"গুরুতর কম্পন: ৮.২Hz নিরাপত্তা সীমা ৭.৫Hz অতিক্রম করেছে"

---

## 🚨 Alert System Usage

### **Alert Types and Responses**

#### **HIGH Risk Alerts (Red)**
**When You Receive:**
- Immediate SMS and email notifications
- Red alert banner on dashboard
- Emergency contact activation

**What to Do:**
1. **EVACUATE IMMEDIATELY** - Remove all personnel from danger zones
2. **STOP ALL EQUIPMENT** - Halt mining operations in affected area
3. **CONTACT EMERGENCY SERVICES** - Call 108 if necessary
4. **ISOLATE AREA** - Prevent access to unstable zones
5. **CONTINUOUS MONITORING** - Switch to real-time sensor checking

**Time to Respond:** <2 minutes

#### **MEDIUM Risk Alerts (Yellow)**
**When You Receive:**
- SMS and email notifications to supervisors
- Yellow indicators on dashboard
- Detailed XAI explanations

**What to Do:**
1. **INCREASE MONITORING** - Check sensors every 2 hours
2. **RESTRICT ACCESS** - Limit personnel in affected areas
3. **BRIEF PERSONNEL** - Update all workers on conditions
4. **REVIEW EQUIPMENT** - Inspect machinery operations
5. **PREPARE EVACUATION** - Ready emergency procedures

**Time to Respond:** <15 minutes

#### **LOW Risk Alerts (Green)**
**When You Receive:**
- Dashboard notifications
- Weekly email summaries
- Standard monitoring alerts

**What to Do:**
1. **ROUTINE MONITORING** - Continue standard sensor checks
2. **NORMAL OPERATIONS** - Maintain regular activities
3. **CONDITION AWARENESS** - Monitor for any changes
4. **DOCUMENTATION** - Log conditions for analysis

**Time to Respond:** Standard operational response

### **Alert Content Examples**

#### **SMS Alert Format:**
```
🚨 ROCKFALL ALERT | शिलाखंड अलर्ट

Mine: Jharia Coalfield
Risk: HIGH | उच्च
Vibration: 8.2Hz
Time: 14:30
Score: 8.7

EVACUATE NOW! | तुरंत निकलें!

- AI Rockfall System
```

#### **Email Alert Format:**
- **Subject**: "🚨 HIGH RISK ALERT - Jharia Coalfield"
- **Content**: 
  - Risk assessment details
  - XAI explanation
  - Contributing factors
  - Threshold violations
  - Recommended actions
  - Emergency contacts
  - System confidence

### **Alert Management**

#### **Acknowledging Alerts:**
1. Click on alert in dashboard
2. Select "Acknowledge Alert"
3. Add notes about actions taken
4. Submit acknowledgment

#### **Resolving Alerts:**
1. Take recommended actions
2. Verify risk reduction
3. Mark alert as resolved
4. Document resolution actions

#### **Alert History:**
- View past alerts in Alerts tab
- Filter by mine, date, or severity
- Export alert reports
- Analyze alert patterns

---

## 🔗 API Reference

### **Authentication Required**
All API endpoints require user authentication. Include session cookies or authentication headers.

### **Base URL**
```
http://localhost:5000/api
```

### **Core Endpoints**

#### **GET /api/mines**
Get list of all mines with current risk levels.

**Response:**
```json
[
  {
    "id": "mine_001",
    "name": "Jharia Coalfield",
    "location": "Dhanbad, Jharkhand",
    "coordinates": [23.7644, 86.4084],
    "current_risk": "MEDIUM",
    "risk_score": 0.456
  }
]
```

#### **GET /api/predictions**
Get current risk predictions for all mines.

**Response:**
```json
[
  {
    "mine_id": "mine_001",
    "mine_name": "Jharia Coalfield",
    "risk_level": "MEDIUM",
    "risk_score": 0.456,
    "confidence": 0.823,
    "timestamp": "2025-09-07T10:30:00Z"
  }
]
```

#### **GET /api/mine/{mine_id}**
Get detailed information for a specific mine.

**Parameters:**
- `mine_id` (string): Mine identifier (e.g., "mine_001")

**Response:**
```json
{
  "mine": {
    "id": "mine_001",
    "name": "Jharia Coalfield",
    "details": "Complete mine information"
  },
  "current_risk": {
    "risk_level": "MEDIUM",
    "risk_score": 0.456
  },
  "realtime_data": {
    "displacement": 2.3,
    "seismic_vibration": 0.45
  }
}
```

#### **GET /api/alerts**
Get current active alerts.

**Response:**
```json
{
  "alerts": [
    {
      "id": "alert_001",
      "mine_id": "mine_001",
      "severity": "HIGH",
      "message": "High rockfall risk detected",
      "timestamp": "2025-09-07T10:30:00Z"
    }
  ]
}
```

#### **GET /api/status**
Get system status and health information.

**Response:**
```json
{
  "status": "healthy",
  "mines_monitored": 18,
  "high_risk": 2,
  "medium_risk": 5,
  "low_risk": 11,
  "models_loaded": true
}
```

### **XAI Endpoints**

#### **GET /api/risk_explanation/{mine_id}**
Get XAI explanation for a mine's risk assessment.

**Response:**
```json
{
  "mine_id": "mine_001",
  "alert_level": "HIGH",
  "primary_explanation": "HIGH RISK: Critical vibration threshold exceeded",
  "contributing_factors": [...],
  "recommendations": [...],
  "confidence_level": 95.2
}
```

#### **GET /api/multilingual_alert/{mine_id}**
Get multilingual alert for a specific mine.

**Response:**
```json
{
  "mine_id": "mine_001",
  "languages": ["hindi", "english"],
  "sms_content": "🚨 शिलाखंड अलर्ट | ROCKFALL ALERT...",
  "risk_factors": {
    "hindi": "कंपन: 8.2Hz",
    "english": "Vibration: 8.2Hz"
  }
}
```

---

## 🔧 Troubleshooting

### **Common Installation Issues**

#### **Python Version Error**
```
Error: Python version 3.8+ required
```
**Solution:**
1. Check Python version: `python --version`
2. Install Python 3.8+ from python.org
3. Use `python3` instead of `python` on macOS/Linux

#### **Package Installation Failures**
```
Error: Failed to install XGBoost
```
**Solution:**
```bash
# Try upgrading pip first
pip install --upgrade pip

# Install specific version
pip install xgboost==1.7.6

# On macOS with Apple Silicon:
pip install --no-use-pep517 xgboost
```

#### **Port Already in Use**
```
Error: Address already in use
```
**Solution:**
```bash
# Find process using port 5000
netstat -ano | findstr :5000    # Windows
lsof -i :5000                   # macOS/Linux

# Kill the process
taskkill /PID <PID_NUMBER> /F   # Windows
kill -9 <PID_NUMBER>           # macOS/Linux

# Or use different port
python app_with_auth.py --port 5001
```

### **Runtime Issues**

#### **Database Connection Error**
```
Error: Unable to open database file
```
**Solution:**
1. Ensure write permissions in `web_app` directory
2. Delete existing `rockfall_system.db` file
3. Restart application (database will be recreated)

#### **Missing Models Error**
```
Error: Model file not found
```
**Solution:**
1. Verify `scripts/` folder contains model files:
   - `rockfall_xgb_final.pkl`
   - `rockfall_model.pkl`
   - `feature_columns.pkl`
2. If missing, the system will use rule-based fallback

#### **Alert System Not Working**
```
Error: Failed to send SMS/Email
```
**Solution:**
1. Check `.env` file configuration
2. Verify email credentials (use app password for Gmail)
3. Test Twilio credentials
4. Check firewall blocking SMTP ports (587, 465)

### **Dashboard Issues**

#### **Map Not Loading**
**Symptoms:** Blank map area or no mine markers
**Solution:**
1. Check internet connection (required for map tiles)
2. Disable ad blockers
3. Try different browser
4. Clear browser cache

#### **Charts Not Displaying**
**Symptoms:** Empty chart areas or loading errors
**Solution:**
1. Check browser console for JavaScript errors
2. Ensure Chart.js CDN is accessible
3. Try refreshing the page
4. Update browser to latest version

#### **Login Issues**
**Symptoms:** Cannot login with demo credentials
**Solution:**
1. Verify username/password exactly as shown:
   - Username: `admin_demo`
   - Password: `Admin@2024`
2. Clear browser cookies
3. Try different browser
4. Check if database file exists and has write permissions

### **Performance Issues**

#### **Slow Dashboard Loading**
**Solution:**
1. Check system resources (CPU, memory)
2. Reduce number of browser tabs
3. Increase system RAM if possible
4. Use Chrome or Firefox for better performance

#### **High Memory Usage**
**Solution:**
1. Close unnecessary applications
2. Reduce update frequency in configuration
3. Restart the application periodically
4. Consider production deployment with more resources

### **XAI Issues**

#### **XAI Explanations Not Showing**
**Symptoms:** Alerts appear but no explanations
**Solution:**
1. Check if XAI is enabled in configuration:
   ```env
   XAI_ENABLED=true
   ```
2. Restart application after configuration change
3. Check console logs for XAI processing errors

#### **Multilingual Text Not Displaying**
**Symptoms:** Question marks instead of regional text
**Solution:**
1. Ensure browser supports Unicode
2. Check system fonts for regional languages
3. Verify UTF-8 encoding in browser
4. Update browser to latest version

### **Getting Help**

#### **System Logs**
Check console output for detailed error messages:
- Start application with: `python app_with_auth.py`
- Look for ERROR or WARNING messages
- Copy error messages for support

#### **Debug Mode**
Enable debug mode for more detailed information:
```env
FLASK_DEBUG=True
```
**Warning:** Only use debug mode for troubleshooting, not production.

#### **Test Scripts**
Run diagnostic tests:
```bash
# Basic system test
python test_system.py

# XAI functionality test  
python test_xai_alerts.py

# Multilingual test
python test_multilingual_sms.py
```

---

## 🔧 Maintenance Guide

### **Regular Maintenance Tasks**

#### **Daily Checks**
- Monitor system logs for errors
- Verify dashboard accessibility
- Check alert delivery status
- Review system performance metrics

#### **Weekly Maintenance**
- Database backup
- Clear old log files
- Update system if needed
- Test alert system functionality

#### **Monthly Maintenance**
- System performance review
- User account audit
- Configuration review
- Documentation updates

### **Database Maintenance**

#### **Backup Database**
```bash
# Copy database file
cp rockfall_system.db rockfall_system_backup.db

# Or with timestamp
cp rockfall_system.db "rockfall_system_$(date +%Y%m%d).db"
```

#### **Clean Old Data**
```sql
-- Connect to database and clean old sessions
sqlite3 rockfall_system.db
DELETE FROM user_sessions WHERE expires < datetime('now');
DELETE FROM login_attempts WHERE timestamp < datetime('now', '-30 days');
.exit
```

### **Performance Monitoring**

#### **Check System Resources**
```bash
# Linux/macOS
top -p $(pgrep -f python)
df -h

# Windows
tasklist /fi "imagename eq python.exe"
```

#### **Monitor Log Files**
- Check application logs for errors
- Monitor disk space usage
- Watch for memory leaks
- Track response times

### **Security Maintenance**

#### **Update Dependencies**
```bash
# Check for outdated packages
pip list --outdated

# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade flask
```

#### **Security Audit**
- Review user accounts regularly
- Monitor login attempts
- Update passwords periodically
- Check for unused accounts

### **Backup and Recovery**

#### **Complete System Backup**
1. **Application Code**: Copy entire `web_app` folder
2. **Database**: Backup `rockfall_system.db` file
3. **Configuration**: Save `.env` file
4. **Custom Models**: Backup any custom model files

#### **Recovery Process**
1. Install Python and dependencies
2. Restore application files
3. Restore database file
4. Restore configuration
5. Test system functionality

---

## 📞 Support and Resources

### **Documentation Resources**
- **README.md**: Quick start guide
- **FINAL_PROJECT_DOCUMENTATION.md**: Complete technical documentation
- **PROJECT_OVERVIEW.md**: Executive summary
- **TECHNICAL_ARCHITECTURE.md**: System architecture details

### **Testing Resources**
- **test_system.py**: Basic system functionality test
- **test_xai_alerts.py**: XAI functionality testing
- **test_multilingual_sms.py**: Multilingual feature testing

### **Configuration Templates**
- **.env.template**: Environment variable template
- **requirements.txt**: Python dependency list
- **start_dashboard.py**: Easy startup script

### **Support Checklist**

Before seeking help, please:
1. ✅ Check this user guide for solutions
2. ✅ Run `python test_system.py` to identify issues
3. ✅ Check console output for error messages
4. ✅ Verify all requirements are met
5. ✅ Try basic troubleshooting steps

### **Common Solutions Summary**

| Issue | Quick Solution |
|-------|---------------|
| **Installation fails** | Upgrade pip, install Python 3.8+ |
| **Port in use** | Kill process or use different port |
| **Login doesn't work** | Check exact credentials, clear cookies |
| **Map not loading** | Check internet, disable ad blocker |
| **Charts not showing** | Update browser, check JavaScript |
| **Alerts not sending** | Verify email/SMS configuration |
| **Slow performance** | Close apps, increase RAM, restart |
| **XAI not working** | Enable in config, restart app |

---

## 🎯 Summary

This comprehensive user guide covers everything needed to install, configure, and use the AI-Based Rockfall Prediction System effectively. The system is designed to be user-friendly while providing powerful mining safety capabilities through AI, XAI explanations, and multilingual support.

### **Key Takeaways**
- **Easy Installation**: Simple pip install process
- **Flexible Configuration**: Customizable via environment variables
- **User-Friendly Interface**: Intuitive dashboard design
- **Comprehensive XAI**: Clear explanations for all risk assessments
- **Multi-Language Support**: Accessible to diverse workforce
- **Production Ready**: Scalable and maintainable architecture

### **Getting Started Quickly**
1. Install Python 3.8+
2. Run `pip install -r requirements.txt`
3. Execute `python app_with_auth.py`
4. Open `http://localhost:5000`
5. Login with demo credentials
6. Explore the interactive dashboard

The system is designed to be operational immediately after installation, with comprehensive testing and fallback systems to ensure reliability. For production deployment or advanced configurations, refer to the technical documentation and architecture guides.

---

**🏆 The AI-Based Rockfall Prediction System is ready to revolutionize mining safety through intelligent, explainable, and accessible technology.**

**Built with ❤️ for Indian Mining Safety | Smart India Hackathon 2024**