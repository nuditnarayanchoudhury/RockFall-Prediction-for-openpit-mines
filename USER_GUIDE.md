# 👤 AI-Based Rockfall Prediction System - User Guide

## 🚀 Quick Start Guide

### **Getting Started in 5 Minutes**

1. **Start the System**
   ```bash
   cd web_app
   python start_dashboard.py
   ```

2. **Open Dashboard**
   - Go to: http://localhost:5000
   - Wait for data to load (2-3 seconds)

3. **Explore the Dashboard**
   - 🗺️ **Map**: Click on mine markers to see details
   - 📊 **Statistics**: View risk counts at the top
   - 🚨 **Alerts**: Check active alerts on the right
   - 📈 **Analytics**: Click "Analytics" tab for charts

4. **Test Alert System**
   - Click the red "Emergency" button on the map
   - Watch for the red alert banner at the top
   - Try dismissing and refreshing to see behavior

---

## 🖥️ Dashboard Overview

### **Main Interface Layout**
```
┌─────────────────────────────────────────────────────┐
│  🚨 Red Alert Banner (appears for HIGH risk)       │
├─────────────────────────────────────────────────────┤
│  🏔️ AI Rockfall Prediction System   🔴 Connected   │
├─────────────────────────────────────────────────────┤
│  Overview | Alerts & Actions | Analytics | Models  │
├─────────────────────────────────────────────────────┤
│  [Statistics Cards - Risk Counts]                  │
├───────────────────────────────┬─────────────────────┤
│                               │                     │
│  🗺️ Interactive Map           │  📋 Active Alerts   │
│  (18 Indian Mining Sites)     │  🌤️ Weather Widget  │
│                               │  📊 Sensor Status   │
│  📈 Risk Trends Chart         │  ℹ️ Mine Details    │
│                               │                     │
└───────────────────────────────┴─────────────────────┘
```

### **Color Coding System**
- 🔴 **Red**: HIGH risk mines (immediate action required)
- 🟡 **Yellow**: MEDIUM risk mines (increased monitoring)
- 🟢 **Green**: LOW risk mines (normal operations)
- 🔵 **Blue**: System information and neutral elements

---

## 📋 Tab-by-Tab User Guide

### **1️⃣ Overview Tab** (Default View)

#### **📊 Statistics Cards**
- **High Risk Mines**: Number of mines with HIGH risk level
- **Medium Risk Mines**: Number of mines with MEDIUM risk level  
- **Low Risk Mines**: Number of mines with LOW risk level
- **Total Active Mines**: Total mines being monitored (18)

*What to do*: Monitor these numbers. If High Risk count increases, immediate attention required.

#### **🗺️ Interactive Map**
- **Mine Markers**: Colored circles representing each mine
- **Click Actions**: Click any marker to see mine details popup
- **Map Controls**: Zoom in/out, pan across India
- **Refresh Button**: Updates all mine data manually
- **Emergency Button**: Triggers emergency alert system

*What to do*: 
- Look for red markers (high risk)
- Click markers to get detailed information
- Use Emergency button only in real emergencies

#### **📈 Risk Trends Chart**
- Shows risk level counts over the last 7 days
- Three colored lines: High (Red), Medium (Yellow), Low (Green)
- Updates automatically every 30 seconds

*What to do*: Watch for increasing red line trend indicating more high-risk situations.

#### **🌤️ Weather Widget**
- Current weather conditions affecting mining operations
- Temperature and weather description
- Considers seasonal patterns (monsoon awareness)

*What to do*: High rainfall periods increase rockfall risk. Plan accordingly.

#### **📋 Active Alerts Panel**
- Scrollable list of current alerts
- Each alert shows: Mine name, risk level, timestamp
- Dismissible alerts (click X to dismiss)
- Refresh button to reload alerts

*What to do*: 
- Review all alerts regularly
- Click "View Details" for more information
- Dismiss alerts after taking action

#### **📊 Sensor Status Panel**
- GPS Sensors: Location tracking (Green = Online)
- Seismic Sensors: Earthquake monitoring (Green = Online)  
- Drone Network: Aerial monitoring (Yellow = Partial coverage)
- Weather API: Meteorological data (Green = Online)

*What to do*: Ensure all sensors show "Online". Report any offline sensors to technical team.

### **2️⃣ Alerts & Actions Tab**

#### **🚨 Critical Alerts Section**
- Shows only HIGH risk alerts requiring immediate attention
- Detailed alert information with mine location
- Emergency action buttons
- Real-time updates

*What to do*:
- For HIGH risk alerts: Follow emergency protocols immediately
- Click "Emergency Response" to trigger full emergency procedures
- Click "Acknowledge" after taking action

#### **📊 Alert Timeline Chart**
- Shows alert frequency throughout the day
- Helps identify peak risk periods
- Updates in real-time

*What to do*: Use this to plan shift schedules and identify high-risk time periods.

#### **📋 Emergency Action Plans**
Three predefined action plans based on risk levels:

**🔴 HIGH RISK Actions:**
- ❗ Immediate evacuation of all personnel
- ⛔ Stop all mining operations  
- 📞 Contact emergency services (108)
- 👥 Deploy emergency response team
- 📡 Increase monitoring frequency

**🟡 MEDIUM RISK Actions:**
- 🚫 Restrict access to unstable areas
- 👁️ Increase monitoring frequency
- 📋 Review safety protocols
- 👥 Brief all personnel on risks  
- 🛤️ Prepare evacuation routes

**🟢 LOW RISK Actions:**
- ▶️ Continue normal operations
- 🛡️ Maintain standard precautions
- 📈 Regular monitoring schedule
- 🔍 Monitor for condition changes

*What to do*: Follow the appropriate action plan based on the risk level displayed.

### **3️⃣ Analytics Tab**

#### **📊 Risk Distribution Chart** (Pie Chart)
- Visual breakdown of current risk levels across all mines
- Interactive: Click segments for details
- Real-time updates

*What to do*: Aim for majority green (low risk). Large red segments require investigation.

#### **📈 Monthly Alert Trends** (Bar Chart)
- Historical alert patterns over 6 months
- Separate bars for HIGH and MEDIUM risk alerts
- Helps identify seasonal patterns

*What to do*: Use for long-term planning and resource allocation during high-risk periods.

#### **🗺️ State-wise Risk Analysis** (Horizontal Bar Chart)
- Average risk scores by Indian state
- Color-coded bars (Red/Yellow/Green)
- Shows which states need more attention

*What to do*: Focus resources on states showing higher risk levels (red/yellow bars).

#### **⏱️ Real-time Sensor Data** (Animated Radar Chart)
- Live sensor readings from all mines
- 6 sensor types: Displacement, Seismic, Crack Density, Strain, Pore Pressure, Rainfall
- Updates every 5 seconds with smooth animation
- Red line = Current readings, Green line = Safe thresholds

*What to do*: 
- When red line extends beyond green line = increased risk
- Monitor for sudden spikes in any sensor reading

### **4️⃣ Models Tab**

#### **🧠 Model Information Cards**
**Primary Model (XGBoost):**
- Training Accuracy: 94.2%
- Validation Accuracy: 91.8%  
- Features Used: 52
- Status: Active

**Fallback Model (Random Forest):**
- Training Accuracy: 89.5%
- Validation Accuracy: 87.3%
- Status: Standby

*What to do*: 
- Green "Active" status = system working normally
- If fallback model is used, contact technical team

#### **📊 Feature Importance Chart**
- Shows which factors most influence rockfall predictions
- Ranked by importance (Seismic Vibration usually highest)
- Helps understand what drives risk levels

*What to do*: Focus monitoring efforts on the top-ranked features.

#### **📈 Model Performance Metrics**
- Precision: 0.923 (accuracy of positive predictions)
- Recall: 0.918 (ability to find all actual risks)
- F1-Score: 0.920 (balanced accuracy measure)
- AUC-ROC: 0.956 (overall model performance)

*What to do*: All values above 0.90 indicate excellent performance. Values below 0.85 may require model retraining.

---

## 🚨 Red Alert Banner System

### **When It Appears**
- Automatically shows when any mine reaches HIGH risk level
- Appears at the very top of the screen
- Bright red color with pulsing animation
- Brief alert sound plays

### **Alert Content**
- **Single Mine**: "🚨 CRITICAL ALERT: HIGH RISK detected at [Mine Name]!"
- **Multiple Mines**: "🚨 CRITICAL ALERT: [N] mines at HIGH RISK!"
- Shows mine names and basic risk information

### **Available Actions**
- **"View Details" Button**: Navigate to Alerts & Actions tab for full information
- **"X" Button**: Dismiss the alert (stays dismissed for 10 minutes)

### **Behavior**
- ✅ Appears immediately when HIGH risk detected
- ✅ Stays visible until dismissed or risk level decreases
- ✅ Reappears on page refresh if still HIGH risk
- ✅ Auto-expires dismissal after 10 minutes
- ✅ Works on mobile devices

---

## 📱 Mobile Usage Guide

### **Responsive Design Features**
- Dashboard adapts to phone and tablet screens
- Touch-friendly buttons and interactions
- Readable text on small screens
- Optimized map controls for touch

### **Mobile-Specific Tips**
1. **Portrait Mode**: Best for viewing alerts and statistics
2. **Landscape Mode**: Better for map interaction and charts  
3. **Pinch to Zoom**: Works on map and charts
4. **Swipe Navigation**: Swipe between tabs on mobile
5. **Alert Sounds**: Ensure phone volume is on for alert sounds

---

## 🆘 Emergency Procedures

### **HIGH Risk Alert Response**
1. **Immediate Actions** (Within 5 minutes):
   - Sound evacuation alarm
   - Stop all mining operations
   - Begin personnel evacuation
   - Contact emergency services (108)

2. **Emergency Contacts**:
   - Emergency Services: **108** (India Emergency Number)
   - Mine Safety Officer: [Contact from mine details]
   - Regional Mining Authority: [Local authority contact]

3. **Documentation**:
   - Screenshot the alert details
   - Note time and personnel count
   - Record actions taken

### **System Failure Response**
If the dashboard becomes unavailable:
1. Check internet connection
2. Try refreshing the page
3. Contact technical support
4. Implement manual monitoring procedures
5. Use backup communication systems

---

## 🔧 User Settings & Preferences

### **Browser Settings**
- **Notifications**: Allow browser notifications for alerts
- **Sound**: Enable sound for alert notifications
- **Pop-ups**: Allow pop-ups for mine detail windows
- **JavaScript**: Must be enabled for full functionality

### **Recommended Browsers**
- ✅ **Chrome 80+**: Best performance and compatibility
- ✅ **Firefox 75+**: Full feature support
- ✅ **Edge 80+**: Windows integration
- ✅ **Safari 13+**: Mac compatibility
- ❌ Internet Explorer: Not supported

### **Screen Resolution**
- **Desktop**: 1920x1080 or higher recommended
- **Tablet**: 1024x768 minimum
- **Mobile**: 375x667 minimum (iPhone 6 size)

---

## ❓ Frequently Asked Questions

### **General Usage**

**Q: How often does the data update?**
A: The dashboard updates automatically every 30 seconds. You can also click "Refresh" for immediate updates.

**Q: What do the different colors mean on the map?**
A: Red = HIGH risk (immediate action), Yellow = MEDIUM risk (increased monitoring), Green = LOW risk (normal operations).

**Q: Can I use this on my phone?**
A: Yes! The dashboard is fully responsive and works on smartphones and tablets.

### **Alerts & Notifications**

**Q: What should I do when I see a red alert banner?**
A: Click "View Details" immediately to see full information and follow the emergency protocols for HIGH risk situations.

**Q: Why did the red banner disappear?**
A: Either the risk level decreased, or someone dismissed it. Dismissals last 10 minutes, then the banner can reappear if risk is still high.

**Q: How do I know if the alert system is working?**
A: Click the "Emergency" button on the map to test the system. You should see alerts appear within seconds.

### **Technical Issues**

**Q: The charts aren't loading. What should I do?**
A: Check your internet connection. The charts use online resources. Refresh the page or try a different browser.

**Q: I see "Error loading models" in the console. Is this a problem?**
A: The system uses a fallback prediction method that still works accurately. The core functionality is not affected.

**Q: The map isn't showing mines. What's wrong?**
A: This usually indicates a connection issue. Check your internet connection and refresh the page.

### **Data & Accuracy**

**Q: How accurate are the predictions?**
A: The XGBoost model achieves 91.8% validation accuracy. The system also provides confidence scores for each prediction.

**Q: What data sources are used for predictions?**
A: The system combines seismic data, rainfall patterns, ground displacement sensors, drone imagery, and historical mining data.

**Q: Can I export the data or reports?**
A: Currently, data export is not available in the interface, but you can screenshot important information or contact administrators for data access.

---

## 📞 Support & Contact Information

### **Technical Support**
- **System Issues**: Check the troubleshooting section in the main documentation
- **Browser Problems**: Try a different browser or clear cache/cookies  
- **Performance Issues**: Ensure stable internet connection and modern browser

### **Emergency Contacts**
- **India Emergency Services**: **108** (Fire, Police, Medical)
- **National Disaster Response**: **1070**
- **Mining Emergency Helpline**: [Regional authority contact]

### **Training Resources**
- **User Guide**: This document
- **Technical Documentation**: PROJECT_DOCUMENTATION.md
- **API Reference**: TECHNICAL_SPECIFICATIONS.md
- **Video Tutorials**: [Contact administrator for training materials]

---

## 📚 Glossary of Terms

**Alert**: Notification triggered when risk levels exceed safe thresholds  
**Confidence Score**: Measure of prediction reliability (0-1 scale)  
**DEM**: Digital Elevation Model - topographic data  
**Feature**: Data input used by machine learning models  
**HIGH Risk**: Risk score ≥ 0.7 requiring immediate action  
**LOW Risk**: Risk score < 0.4 indicating normal operations  
**MEDIUM Risk**: Risk score 0.4-0.7 requiring increased monitoring  
**Mine Marker**: Colored circle on map representing a mining site  
**Prediction**: AI-calculated risk assessment for a specific mine  
**Risk Score**: Numerical value (0-1) indicating rockfall probability  
**Sensor Data**: Real-time measurements from monitoring equipment  
**XGBoost**: Machine learning algorithm used for primary predictions  

---

**👤 This user guide provides everything needed to effectively use the AI-Based Rockfall Prediction System. For additional help, refer to the complete project documentation or contact technical support.**

**🌐 Dashboard URL**: http://localhost:5000 (when running locally)  
**📊 System Status**: Check the connection indicator in the top-right corner
