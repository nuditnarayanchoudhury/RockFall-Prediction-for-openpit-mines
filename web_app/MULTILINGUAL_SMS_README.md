# Area-Based Multilingual SMS Alert System

## Overview

The SMS alert system now supports automatic language selection based on the mining area/state location. This ensures workers receive critical rockfall alerts in their local language alongside Hindi and English for maximum comprehension and faster response.

## Supported Languages & Regions

### State-wise Language Mapping

| State | Primary Language | SMS Languages |
|-------|-----------------|---------------|
| **West Bengal** | Bengali | Bengali + Hindi + English |
| **Odisha** | Odia | Odia + Hindi + English |
| **Karnataka** | Kannada | Kannada + Hindi + English |
| **Telangana** | Telugu | Telugu + Hindi + English |
| **Andhra Pradesh** | Telugu | Telugu + Hindi + English |
| **Gujarat** | Gujarati | Gujarati + Hindi + English |
| **Maharashtra** | Marathi | Marathi + Hindi + English |
| **Jharkhand** | Hindi | Hindi + English |
| **Chhattisgarh** | Hindi | Hindi + English |
| **Madhya Pradesh** | Hindi | Hindi + English |
| **Rajasthan** | Hindi | Hindi + English |
| **Other/Unknown** | Hindi | Hindi + English (default) |

## SMS Message Format

### Trilingual Example (Odisha Mine)
```
🚨 ପଥର ଖସିବା ଚେତାବନୀ | शिलाखंड अलर्ट | ROCKFALL ALERT

ଖଣି | खान | Mine: Keonjhar Iron Mine
ବିପଦ | जोखिम | Risk: ଅଧିକ ବିପଦ | अत्यधिक खतरा | HIGH RISK
ସମୟ | समय | Time: 14:30
ସ୍କୋର | स्कोर | Score: 8.7

ତତକ୍ଷଣାତ ବାହାରିଯାଆନ୍ତୁ! କାମ ବନ୍ଦ କରନ୍ତୁ! | तुरंत निकासी करें! ऑपरेशन बंद करें! | EVACUATE NOW! Stop operations!

- AI ପଥର ଖସିବା ସିଷ୍ଟମ | AI शिलाखंड सिस्टम | AI Rockfall System
```

### Bilingual Example (Jharkhand Mine)
```
🚨 शिलाखंड अलर्ट | ROCKFALL ALERT

खान | Mine: Ranchi Coal Mine
जोखिम | Risk: अत्यधिक खतरा | HIGH RISK
समय | Time: 14:30
स्कोर | Score: 8.7

तुरंत निकासी करें! ऑपरेशन बंद करें! | EVACUATE NOW! Stop operations!

- AI शिलाखंड सिस्टम | AI Rockfall System
```

## How It Works

### 1. Location Detection
- System extracts state information from mine location data
- Uses pattern matching on location strings (case-insensitive)
- Falls back to Hindi+English for unknown locations

### 2. Language Selection
- Maps detected state to appropriate language combination
- Always includes Hindi and English for broad comprehension
- Adds regional language as primary language where applicable

### 3. Message Generation
- Generates trilingual messages for states with local languages
- Uses pipe separator (|) between language versions
- Maintains consistent structure across all language combinations

## Risk Level Actions

### High Risk (अत्यधिक खतरा)
- **English**: "EVACUATE NOW! Stop operations!"
- **Hindi**: "तुरंत निकासी करें! ऑपरेशन बंद करें!"
- **Bengali**: "এখনই সরে যান! কাজ বন্ধ করুন!"
- **Odia**: "ତତକ୍ଷଣାତ ବାହାରିଯାଆନ୍ତୁ! କାମ ବନ୍ଦ କରନ୍ତୁ!"
- **Kannada**: "ತಕ್ಷಣವೇ ಹೊರಬರಿ! ಕೆಲಸ ನಿಲ್ಲಿಸಿ!"
- **Telugu**: "వెంటనే బయటకు వెళ్లండి! పని ఆపండి!"
- **Gujarati**: "તુરંત બહાર નીકળો! કામ બંધ કરો!"
- **Marathi**: "ताबडतोब बाहेर पडा! काम बंद करा!"

### Medium Risk (मध्यम खतरा)
- Focus on access restriction and increased monitoring

### Low Risk (कम खतरा)  
- Cautious continuation with regular monitoring

## Configuration

### Adding New States
To add support for a new state/region:

1. **Update State Mapping** (`extract_state_from_location`):
```python
'new state': 'NEW_STATE_CODE'
```

2. **Add Language Configuration** (`get_area_languages`):
```python
'NEW_STATE_CODE': ['local_language', 'hindi', 'english']
```

3. **Add Language Translations** (`get_language_translations`):
```python
'local_language': {
    'alert_header': 'Local Alert Header',
    'mine': 'Local Mine Term',
    # ... other translations
}
```

## Technical Features

### Backward Compatibility
- Original bilingual Hindi+English functionality preserved
- Existing SMS endpoints continue to work
- No breaking changes to API

### Performance
- Efficient state detection using lowercase matching
- Cached language translations
- Minimal overhead for message generation

### Extensibility
- Easy to add new languages and states
- Modular translation system
- Flexible language combination logic

## Testing

Run the comprehensive test suite:
```bash
python test_multilingual_sms.py
```

This validates:
- ✅ State extraction from mine locations
- ✅ Language selection for each region
- ✅ SMS message generation in all language combinations
- ✅ Risk level translations and actions
- ✅ Fallback behavior for unknown locations

## Benefits

### Safety Improvements
- **Faster Comprehension**: Workers understand alerts in their native language
- **Reduced Confusion**: Multi-language format prevents misinterpretation
- **Broader Coverage**: Hindi+English ensures understanding even if local language isn't known

### Operational Benefits
- **Automatic Detection**: No manual language configuration required
- **Consistent Format**: Standardized message structure across all regions
- **Scalable**: Easy to add new mining regions and languages

### Regulatory Compliance
- Meets multilingual communication requirements
- Supports diverse workforce in Indian mining industry
- Enhances safety protocol adherence

---

## Implementation Summary

The area-based multilingual SMS system represents a significant enhancement to mine safety communications, ensuring critical rockfall alerts reach workers in a language they understand best, while maintaining the reliability and consistency of the AI-powered early warning system.

For technical support or feature requests, contact the development team.
