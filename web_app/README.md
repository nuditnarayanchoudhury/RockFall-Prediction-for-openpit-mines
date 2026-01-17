# AI-Based Rockfall Prediction System - Web Dashboard v2.0

A comprehensive web-based dashboard for monitoring and predicting rockfall risks across Indian open-pit mines using AI/ML models, real-time sensor data, **Explainable AI (XAI)**, **multilingual alert systems**, and secure user authentication.

## 🆕 What's New in v2.0

### ✨ **Explainable AI (XAI) - The Game Changer**
- **WHY Analysis**: Mine operators now see exactly WHY there's high risk, not just that there is risk
- **Sensor-Level Explanations**: "Critical vibration at 8.2Hz (exceeds 7.5 threshold)"
- **AI Recommendations**: "Inspect vibration sensors, stop Excavator-01, evacuate Block A"
- **Confidence Scoring**: System reliability assessment (0-100%)

### 🌐 **Multilingual Alert System**
- **8 Regional Languages**: Hindi, English, Bengali, Odia, Gujarati, Marathi, Kannada, Telugu
- **Area-Based Selection**: Automatically selects languages based on mine location
- **Smart Translation**: Technical sensor readings explained in local languages

## Features

### 🔐 User Authentication & Security
- **Secure Login System**: Modern label-free forms with password visibility toggle
- **User Registration**: Comprehensive signup with role-based account creation
- **Role-Based Access Control**: Admin, Supervisor, Operator, and Emergency roles
- **Session Management**: Secure session handling with remember-me functionality
- **Account Security**: Login attempt monitoring, account lockout protection
- **Navigation Integration**: User-friendly logout functionality in dashboard navigation

### 🗺️ Interactive Mine Monitoring
- **Live Risk Map**: Interactive map displaying all 18 major Indian open-pit mines with real-time risk indicators
- **Mine Details**: Detailed information panels for each mine including location, operator, type, and current sensor readings
- **Risk Visualization**: Color-coded markers (Red: High Risk, Yellow: Medium Risk, Green: Low Risk)

### 📊 Real-Time Data Integration
- **Multi-Source Data**: Integrates DEM, seismic, rainfall, geotechnical, and drone imagery data
- **Live Updates**: WebSocket-based real-time updates every 30 seconds
- **Historical Trends**: 7-day trend analysis with interactive charts

### 🚨 Advanced Alert System (Enhanced with XAI)
- **🆕 XAI-Enhanced Alerts**: Detailed explanations of WHY there's high risk
- **🆕 Multilingual Support**: 8+ Indian regional languages based on mine location
- **🆕 Smart Recommendations**: AI-generated action items ("Inspect vibration sensors")
- **🆕 Confidence Indicators**: System reliability scores for each alert
- **Multi-Channel Alerts**: Email and SMS notifications based on risk levels
- **Intelligent Routing**: Risk-based recipient targeting (Emergency, Managers, Operators)
- **Rich Notifications**: HTML email alerts with detailed XAI analysis
- **Alert Management**: Alert acknowledgment, resolution tracking, and statistics

### 🤖 AI-Powered Predictions
- **ML Models**: XGBoost and Random Forest models for rockfall prediction
- **Feature Engineering**: 50+ engineered features from multi-source data
- **Confidence Scoring**: Model confidence measures for prediction reliability
- **Risk Categorization**: Automated LOW/MEDIUM/HIGH risk classification

### 📱 Responsive Dashboard
- **Modern UI**: Bootstrap 5-based responsive design
- **Real-Time Charts**: Chart.js integration for trend visualization
- **Mobile Friendly**: Works seamlessly across devices
- **Live Status**: Connection status indicators and health monitoring

## Architecture

```
web_app/
├── app_with_auth.py       # Main Flask application with authentication
├── models.py              # Database models for users and sessions
├── forms.py               # WTForms for login, signup, and user management
├── prediction_service.py  # ML model integration and risk prediction
├── data_service.py        # Indian mines database and data simulation
├── alert_service.py       # Multi-channel alert system (Email/SMS)
├── templates/
│   ├── dashboard.html     # Interactive web dashboard with logout
│   ├── login.html         # Modern label-free login form
│   └── signup.html        # Comprehensive registration form
├── requirements.txt       # Python dependencies (includes authentication)
├── .env.template         # Environment configuration template
└── README.md             # This file
```

## Quick Start

### 1. Install Dependencies
```bash
cd web_app
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy template and edit with your credentials
cp .env.template .env
# Edit .env with your email/SMS API credentials
```

### 3. Run Application
```bash
python app_with_auth.py
```

### 4. Access Dashboard
Open your browser to `http://localhost:5000`. You'll be redirected to the login page.

### 5. Demo Accounts
Use these demo accounts to test the system:
- **Admin**: `admin_demo` / `Admin@2024`
- **Supervisor**: `supervisor_demo` / `Super@2024` 
- **Operator**: `operator_demo` / `Oper@2024`
- **Emergency**: `emergency_demo` / `Emerg@2024`

## Indian Mining Sites Database

The system includes a comprehensive database of 18 major Indian open-pit mines across 11 states:

| State | Mines | Primary Minerals |
|-------|--------|------------------|
| Jharkhand | 3 | Coal |
| Odisha | 3 | Iron Ore, Coal |
| Chhattisgarh | 2 | Coal |
| Rajasthan | 2 | Lead-Zinc |
| Gujarat | 1 | Lignite |
| West Bengal | 1 | Coal |
| Maharashtra | 1 | Coal |
| Karnataka | 1 | Iron Ore |
| Telangana | 1 | Coal |
| Andhra Pradesh | 1 | Limestone |
| Madhya Pradesh | 2 | Diamond, Coal |

## API Endpoints

### Authentication
- `GET /login` - Login page with modern label-free forms
- `POST /login` - User authentication endpoint
- `GET /signup` - User registration page
- `POST /signup` - New user registration
- `GET /logout` - User logout and session cleanup
- `GET /profile` - User profile management

### Mine Data (Protected)
- `GET /api/mines` - List mines with user access filtering
- `GET /api/mine/{mine_id}` - Detailed mine information (access controlled)
- `GET /api/predictions` - Current risk predictions (role-based)

### Alerts (Protected)
- `GET /api/alerts` - Active alerts with user access filtering
- `POST /api/send_test_alert` - Send test alert (requires permissions)

### System (Protected)
- `GET /api/status` - System status with user information
- `GET /api/model_info` - Model information (admin/supervisor only)

### Real-Time
- Authentication-protected API endpoints
- Automatic 30-second refresh cycles
- Role-based data filtering

## Configuration

### Email Alerts
Set up email credentials in `.env`:
```
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### SMS Alerts (Twilio)
Configure Twilio credentials:
```
TWILIO_SID=your_twilio_account_sid
TWILIO_TOKEN=your_twilio_auth_token
TWILIO_PHONE=your_twilio_phone_number
```

### Risk Thresholds
Customize risk classification:
```
HIGH_RISK_THRESHOLD=0.7
MEDIUM_RISK_THRESHOLD=0.4
CONFIDENCE_THRESHOLD=0.6
```

## Alert System

### Risk-Based Routing
- **HIGH Risk**: Emergency contacts + Managers + Operators
- **MEDIUM Risk**: Managers + Operators  
- **LOW Risk**: Operators only

### Alert Channels
1. **Email**: Rich HTML notifications with risk factors and actions
2. **SMS**: Concise text alerts for high-priority situations
3. **Dashboard**: Real-time visual notifications

### Alert Content
Each alert includes:
- Mine information and location
- Risk level and score
- Key contributing factors
- Recommended immediate actions
- Timestamp and tracking ID

## Data Simulation

For demonstration purposes, the system includes realistic data simulation:
- **Geospatial**: Coordinates, elevation, slope data
- **Seismic**: Earthquake magnitude, depth, station data
- **Weather**: Monthly rainfall patterns by region
- **Geotechnical**: Displacement, strain, pore pressure
- **Drone**: Crack density, vegetation coverage, debris analysis

## ML Model Integration

### Supported Models
1. **XGBoost**: Primary model (rockfall_xgb_final.pkl)
2. **Random Forest**: Fallback model (rockfall_model.pkl)
3. **Feature Columns**: Trained feature set (feature_columns.pkl)

### Feature Engineering
The system automatically prepares 50+ features including:
- Temporal features (season, month, year)
- Geospatial coordinates and terrain
- Seismic activity parameters
- Monthly and seasonal rainfall
- Geotechnical sensor readings
- Drone-derived imagery features

### Fallback Prediction
When trained models are unavailable, the system uses rule-based risk calculation considering:
- Seismic vibration levels
- Crack density thresholds
- Slope stability factors
- Displacement measurements
- Rainfall intensity

## Security Considerations

### Authentication & Authorization
- **Flask-Login**: Secure session management
- **Password Hashing**: Werkzeug PBKDF2 with salt
- **CSRF Protection**: WTForms CSRF tokens on all forms
- **Role-Based Access**: Different permission levels for users
- **Login Monitoring**: Failed attempt tracking and account lockout
- **Session Security**: Configurable session timeouts and cleanup

### Application Security
- Environment variables for sensitive credentials
- Input validation for API endpoints and forms
- Rate limiting for alert systems
- SQL injection protection via SQLAlchemy ORM
- Data sanitization for dashboard display
- Secure form validation with WTForms

## Future Enhancements

### Completed Features ✅
- [x] **User authentication and role-based access** - Complete with login/signup
- [x] **Database integration** - SQLite with user sessions and login tracking
- [x] **Modern UI/UX** - Label-free forms with professional styling

### Planned Features
- [ ] Historical data analytics and reporting dashboard
- [ ] Mobile app development (React Native/Flutter)
- [ ] Advanced weather API integration (real weather data)
- [ ] Machine learning model retraining pipeline
- [ ] Geographical clustering and zone management
- [ ] Emergency evacuation route planning
- [ ] Multi-language support (Hindi, English)
- [ ] Advanced user management (password reset via email)

### Integration Opportunities
- Government mining databases
- Real-time weather services
- Seismic monitoring networks
- Satellite imagery providers
- Emergency response systems

## Support

For technical issues or feature requests, please refer to the project documentation or contact the development team.

## License

This project is developed for the Smart India Hackathon (SIH) initiative to improve mining safety through AI-powered risk prediction systems.
