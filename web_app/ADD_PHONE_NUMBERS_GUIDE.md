# 📱 Adding Additional Phone Numbers to SMS Alerts

## 🎯 **Current Status:**
- ✅ **7735776771**: Working (verified)
- ⚠️ **7815015581**: Needs verification
- ⚠️ **9078280686**: Needs verification

## 🔧 **How to Add the Additional Numbers:**

### **Step 1: Verify Numbers in Twilio Console**

1. **Go to**: [Twilio Console - Phone Numbers](https://console.twilio.com/us1/develop/phone-numbers/manage/verified)
2. **Login** with your Twilio account
3. **Click**: "Verify a new number" or similar button
4. **Enter**: `+917815015581`
5. **Enter**: `+919078280686`
6. **Process**: Each number will receive an OTP via SMS for verification

### **Step 2: Update Configuration**

After both numbers are verified in Twilio:

1. **Open**: `.env` file
2. **Comment out current lines**:
   ```bash
   # EMERGENCY_PHONES=+917735776771
   # MANAGER_PHONES=+917735776771
   # OPERATOR_PHONES=+917735776771
   ```

3. **Uncomment the multi-number lines**:
   ```bash
   EMERGENCY_PHONES=+917735776771,+917815015581,+919078280686
   MANAGER_PHONES=+917735776771,+917815015581,+919078280686
   OPERATOR_PHONES=+917735776771,+917815015581,+919078280686
   ```

### **Step 3: Test Multi-Number SMS**

```bash
python test_multiple_sms.py
```

## 💰 **Alternative: Upgrade to Paid Account**

If you upgrade your Twilio account (add $20+ credit):
- ✅ Send SMS to **any** phone number (no verification needed)
- ✅ Remove "Sent from trial account" message
- ✅ Higher rate limits

## 🚀 **Current System Status:**

Right now, your system **IS WORKING** and sending alerts to:
- 📱 **7735776771** ✅

When HIGH risk is detected at any mining site, this number receives immediate SMS alerts like:

```
🚨 ROCKFALL ALERT
Mine: Jharia Coalfield
Risk: HIGH
Time: 20:16
Score: 0.85

EVACUATE NOW! Stop operations.

- AI Rockfall System
```

## ⚡ **Quick Actions:**

### **Option A: Keep Current Setup (Working Now)**
- System sends SMS to **7735776771**
- You can manually forward critical alerts to team members
- **No additional setup needed**

### **Option B: Verify Additional Numbers (FREE)**
- Takes ~5 minutes to verify each number in Twilio Console
- Then update `.env` file as shown above
- All three numbers receive automatic alerts

### **Option C: Upgrade Twilio Account (~$20)**
- Send SMS to any number without verification
- Professional SMS (no "trial account" message)
- Higher SMS limits

## 🎯 **Recommendation:**

**For immediate use**: Your system is already working perfectly with one number!

**For team alerts**: Verify the two additional numbers (takes ~10 minutes total)

## ✅ **Current Automatic Alerts Working:**

Your system is **already detecting HIGH risk mines and sending SMS alerts** to 7735776771. Check the terminal logs - you should see:

```
🚨 AUTOMATIC ALERT SENT: [Mine Name] - HIGH RISK
Alert channels used: ['SMS']
```

**Your automation is live and working!** 🎉
