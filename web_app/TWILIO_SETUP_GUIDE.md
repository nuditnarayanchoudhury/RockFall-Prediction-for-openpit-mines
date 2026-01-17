# 📱 Twilio SMS Setup Guide for AI Rockfall Prediction System

## 🚀 **Quick Setup Steps**

### **Step 1: Create Twilio Account (FREE)**

1. **Visit**: [https://www.twilio.com](https://www.twilio.com)
2. **Click**: "Try Twilio free" button
3. **Sign Up**: Use your email: `23cseds052.subhamkumarmohanty@giet.edu`
4. **Verify Phone**: Enter your number: `+917735776771`
5. **Complete Registration**: Fill in details

### **Step 2: Get Your FREE Trial Credits**

- ✅ **$15 FREE** credit for new accounts
- ✅ **FREE Twilio phone number**
- ✅ **FREE SMS to verified numbers**

### **Step 3: Get Your Credentials from Console**

After logging in to [Twilio Console](https://console.twilio.com):

1. **Account SID** (looks like): `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
2. **Auth Token** (click eye icon to reveal): `your_auth_token_here`
3. **Your Twilio Phone Number**: Get from Phone Numbers section

### **Step 4: Configure Your .env File**

Open your `.env` file and replace:

```bash
# Replace these with your actual Twilio credentials
TWILIO_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_TOKEN=your_actual_auth_token_from_twilio
TWILIO_PHONE=+1234567890
```

### **Step 5: Update Phone Number Recipients**

Your phone number `+917735776771` is already configured in:

```bash
EMERGENCY_PHONES=+917735776771
MANAGER_PHONES=+917735776771  
OPERATOR_PHONES=+917735776771
```

### **Step 6: Test SMS Configuration**

Run this test script to verify SMS works:

```python
# Create test_sms.py
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

# Your credentials
account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_TOKEN')
twilio_phone = os.getenv('TWILIO_PHONE')
your_phone = '+917735776771'

client = Client(account_sid, auth_token)

message = client.messages.create(
    body='🚨 TEST: AI Rockfall System SMS alerts are working! This confirms HIGH risk alerts will be sent to your phone.',
    from_=twilio_phone,
    to=your_phone
)

print(f"✅ Test SMS sent! Message SID: {message.sid}")
```

## 🔧 **Detailed Configuration**

### **What You'll Get from Twilio Console:**

1. **Account SID**: 
   - Location: Dashboard → Account Info
   - Format: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Example: `AC1234567890abcdef1234567890abcdef`

2. **Auth Token**:
   - Location: Dashboard → Account Info (click eye icon)
   - Format: `32-character string`
   - Example: `abcdef1234567890abcdef1234567890`

3. **Twilio Phone Number**:
   - Location: Phone Numbers → Manage → Active numbers
   - Format: `+1234567890` (US number for free trial)
   - Example: `+15551234567`

### **Update Your .env File:**

```bash
# SMS Configuration (Replace with your actual values)
TWILIO_SID=AC1234567890abcdef1234567890abcdef
TWILIO_TOKEN=abcdef1234567890abcdef1234567890
TWILIO_PHONE=+15551234567

# Your phone number (already configured)
EMERGENCY_PHONES=+917735776771
MANAGER_PHONES=+917735776771
OPERATOR_PHONES=+917735776771
```

## 🧪 **Testing SMS Alerts**

### **Method 1: Use Test Script**

Create `test_sms.py`:

```python
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

try:
    client = Client(os.getenv('TWILIO_SID'), os.getenv('TWILIO_TOKEN'))
    
    message = client.messages.create(
        body='🚨 Rockfall Alert Test: Your SMS system is working!',
        from_=os.getenv('TWILIO_PHONE'),
        to='+917735776771'
    )
    
    print(f"✅ SMS sent successfully! Message ID: {message.sid}")
    
except Exception as e:
    print(f"❌ SMS failed: {e}")
```

Run: `python test_sms.py`

### **Method 2: Use Built-in System Test**

```python
# Run the main app and it will automatically try to send SMS for HIGH risk alerts
python app_with_auth.py
```

## 📋 **SMS Alert Examples**

When HIGH risk is detected, you'll receive SMS like:

```
🚨 ROCKFALL ALERT
Mine: Jharia Coalfields
Risk: HIGH  
Time: 14:30
Score: 0.85

EVACUATE NOW! Stop operations.

- AI Rockfall System
```

## 💰 **Cost Information**

- **Free Trial**: $15 credit (enough for ~750 SMS messages)
- **SMS Cost**: ~$0.02 per SMS to India
- **Monthly Cost**: ~$1 for phone number (after trial)

## 🔧 **Troubleshooting**

### **Common Issues:**

1. **"Account not found"**: Check Account SID
2. **"Authentication failed"**: Check Auth Token
3. **"From number not verified"**: Use your Twilio phone number
4. **"To number not verified"**: In trial, verify +917735776771 in Twilio Console

### **Trial Limitations:**

- ✅ Can send to verified numbers (your phone: +917735776771)
- ⚠️ Cannot send to unverified numbers during trial
- ✅ All messages include "Sent from your Twilio trial account"
- ✅ $15 free credit included

## 🎯 **Final Configuration Check**

After setup, your `.env` should look like:

```bash
# Email Configuration
EMAIL_USER=23cseds052.subhamkumarmohanty@giet.edu
EMAIL_PASSWORD=Subham.123

# SMS Configuration  
TWILIO_SID=ACyour_actual_account_sid_here
TWILIO_TOKEN=your_actual_auth_token_here
TWILIO_PHONE=+1your_twilio_number_here

# Your phone for alerts
EMERGENCY_PHONES=+917735776771
```

## ✅ **Success Indicators**

When working correctly, you'll see in logs:

```
✅ Automatic alert monitoring started
📧 Email alert sent successfully
📱 SMS alert sent successfully  
🚨 AUTOMATIC ALERT SENT: [Mine Name] - HIGH RISK
```

---

## 🆘 **Need Help?**

If you encounter issues:

1. **Check Twilio Console** for error messages
2. **Verify phone number** format (+917735776771)
3. **Ensure free trial credits** are available
4. **Test with the test script** first

Your system will now send **both EMAIL and SMS alerts** when HIGH risk conditions are detected! 🎉
