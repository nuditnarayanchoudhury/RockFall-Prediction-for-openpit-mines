#!/usr/bin/env python3
"""
XAI Risk Explanation Module for Rockfall Alert System

This module provides explainable AI functionality to help mine operators understand
why the system determined a particular risk level, what factors contributed to the 
assessment, and what specific conditions triggered the alert.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional

class RockfallRiskExplainer:
    """Explainable AI module for rockfall risk assessment"""
    
    def __init__(self):
        self.risk_thresholds = self._load_risk_thresholds()
        self.factor_weights = self._load_factor_weights()
        self.historical_baselines = self._load_historical_baselines()
    
    def _load_risk_thresholds(self) -> Dict:
        """Load risk assessment thresholds for different sensor types"""
        return {
            'vibration': {
                'low': {'min': 0.0, 'max': 2.5},
                'medium': {'min': 2.5, 'max': 5.0},
                'high': {'min': 5.0, 'max': float('inf')},
                'critical': {'min': 7.5, 'max': float('inf')}
            },
            'temperature': {
                'low': {'min': 15.0, 'max': 30.0},
                'medium': {'min': 30.0, 'max': 40.0}, 
                'high': {'min': 40.0, 'max': 50.0},
                'critical': {'min': 50.0, 'max': float('inf')}
            },
            'humidity': {
                'low': {'min': 30.0, 'max': 70.0},
                'medium': {'min': 70.0, 'max': 85.0},
                'high': {'min': 85.0, 'max': 95.0},
                'critical': {'min': 95.0, 'max': float('inf')}
            },
            'pressure': {
                'low': {'min': 980.0, 'max': 1020.0},
                'medium': {'min': 1020.0, 'max': 1040.0},
                'high': {'min': 1040.0, 'max': 1060.0},
                'critical': {'min': 1060.0, 'max': float('inf')}
            },
            'acoustic': {
                'low': {'min': 30.0, 'max': 60.0},
                'medium': {'min': 60.0, 'max': 80.0},
                'high': {'min': 80.0, 'max': 100.0},
                'critical': {'min': 100.0, 'max': float('inf')}
            },
            'slope_stability': {
                'low': {'min': 0.0, 'max': 0.1},
                'medium': {'min': 0.1, 'max': 0.3},
                'high': {'min': 0.3, 'max': 0.5},
                'critical': {'min': 0.5, 'max': float('inf')}
            }
        }
    
    def _load_factor_weights(self) -> Dict:
        """Load importance weights for different risk factors"""
        return {
            'vibration': 0.30,      # Highest weight - direct indicator of instability
            'slope_stability': 0.25, # Second highest - geological assessment
            'acoustic': 0.15,       # Sound patterns indicate stress
            'pressure': 0.10,       # Atmospheric pressure changes
            'temperature': 0.10,    # Thermal expansion effects
            'humidity': 0.05,       # Moisture impact on rock integrity
            'trend': 0.05          # Historical trend analysis
        }
    
    def _load_historical_baselines(self) -> Dict:
        """Load historical baseline values for comparison"""
        return {
            'vibration_baseline': 1.2,
            'temperature_baseline': 25.0,
            'humidity_baseline': 45.0,
            'pressure_baseline': 1013.25,
            'acoustic_baseline': 45.0,
            'slope_stability_baseline': 0.05
        }
    
    def explain_risk_assessment(self, sensor_data: Dict, risk_score: float, alert_level: str, 
                              historical_data: Optional[List] = None) -> Dict:
        """
        Generate comprehensive explanation for risk assessment
        
        Args:
            sensor_data: Current sensor readings
            risk_score: Calculated risk score (0-10)
            alert_level: HIGH/MEDIUM/LOW
            historical_data: Optional historical sensor data for trend analysis
            
        Returns:
            Dictionary containing detailed risk explanation
        """
        
        # Analyze individual sensor contributions
        sensor_analysis = self._analyze_sensor_contributions(sensor_data)
        
        # Determine primary risk factors
        primary_factors = self._identify_primary_factors(sensor_analysis, risk_score)
        
        # Generate trend analysis if historical data available
        trend_analysis = self._analyze_trends(sensor_data, historical_data) if historical_data else None
        
        # Create threshold violations summary
        threshold_violations = self._check_threshold_violations(sensor_data)
        
        # Generate risk explanation narrative
        explanation_text = self._generate_explanation_narrative(
            sensor_analysis, primary_factors, threshold_violations, alert_level
        )
        
        # Create actionable recommendations
        recommendations = self._generate_recommendations(
            primary_factors, threshold_violations, alert_level
        )
        
        return {
            'alert_level': alert_level,
            'risk_score': risk_score,
            'primary_explanation': explanation_text,
            'contributing_factors': primary_factors,
            'sensor_analysis': sensor_analysis,
            'threshold_violations': threshold_violations,
            'trend_analysis': trend_analysis,
            'recommendations': recommendations,
            'confidence_level': self._calculate_confidence(sensor_analysis),
            'timestamp': datetime.now().isoformat()
        }
    
    def _analyze_sensor_contributions(self, sensor_data: Dict) -> Dict:
        """Analyze how each sensor contributes to overall risk"""
        contributions = {}
        
        for sensor_type, value in sensor_data.items():
            if sensor_type in self.risk_thresholds:
                # Determine risk level for this sensor
                sensor_risk_level = self._get_sensor_risk_level(sensor_type, value)
                
                # Calculate contribution score
                contribution_score = self._calculate_sensor_contribution(sensor_type, value, sensor_risk_level)
                
                # Get baseline comparison
                baseline_comparison = self._compare_to_baseline(sensor_type, value)
                
                contributions[sensor_type] = {
                    'current_value': value,
                    'risk_level': sensor_risk_level,
                    'contribution_score': contribution_score,
                    'baseline_comparison': baseline_comparison,
                    'threshold_status': self._get_threshold_status(sensor_type, value),
                    'weight': self.factor_weights.get(sensor_type, 0.1)
                }
        
        return contributions
    
    def _get_sensor_risk_level(self, sensor_type: str, value: float) -> str:
        """Determine risk level for a specific sensor reading"""
        thresholds = self.risk_thresholds.get(sensor_type, {})
        
        if value >= thresholds.get('critical', {}).get('min', float('inf')):
            return 'critical'
        elif value >= thresholds.get('high', {}).get('min', float('inf')):
            return 'high'
        elif value >= thresholds.get('medium', {}).get('min', float('inf')):
            return 'medium'
        else:
            return 'low'
    
    def _calculate_sensor_contribution(self, sensor_type: str, value: float, risk_level: str) -> float:
        """Calculate how much this sensor contributes to overall risk (0-10 scale)"""
        weight = self.factor_weights.get(sensor_type, 0.1)
        
        risk_multipliers = {
            'low': 1.0,
            'medium': 3.0,
            'high': 6.0,
            'critical': 10.0
        }
        
        base_contribution = risk_multipliers.get(risk_level, 1.0)
        return min(10.0, base_contribution * weight * 10)
    
    def _compare_to_baseline(self, sensor_type: str, value: float) -> Dict:
        """Compare current reading to historical baseline"""
        baseline_key = f"{sensor_type}_baseline"
        baseline = self.historical_baselines.get(baseline_key, value)
        
        if baseline == 0:
            percentage_change = 0
        else:
            percentage_change = ((value - baseline) / baseline) * 100
        
        return {
            'baseline_value': baseline,
            'current_value': value,
            'absolute_change': value - baseline,
            'percentage_change': round(percentage_change, 1),
            'status': 'above_baseline' if value > baseline else 'below_baseline' if value < baseline else 'at_baseline'
        }
    
    def _get_threshold_status(self, sensor_type: str, value: float) -> Dict:
        """Get detailed threshold status for a sensor"""
        thresholds = self.risk_thresholds.get(sensor_type, {})
        current_level = self._get_sensor_risk_level(sensor_type, value)
        
        # Find next threshold
        next_threshold = None
        if current_level == 'low':
            next_threshold = thresholds.get('medium', {}).get('min')
        elif current_level == 'medium':
            next_threshold = thresholds.get('high', {}).get('min')
        elif current_level == 'high':
            next_threshold = thresholds.get('critical', {}).get('min')
        
        return {
            'current_level': current_level,
            'next_threshold': next_threshold,
            'margin_to_next': next_threshold - value if next_threshold else None,
            'percentage_to_next': ((value / next_threshold) * 100) if next_threshold and next_threshold > 0 else None
        }
    
    def _identify_primary_factors(self, sensor_analysis: Dict, risk_score: float) -> List[Dict]:
        """Identify the primary factors contributing to risk"""
        factors = []
        
        # Sort sensors by contribution score
        sorted_sensors = sorted(
            sensor_analysis.items(),
            key=lambda x: x[1]['contribution_score'],
            reverse=True
        )
        
        # Take top contributing factors (those with significant contribution)
        for sensor_type, analysis in sorted_sensors:
            if analysis['contribution_score'] > 1.0:  # Significant contribution threshold
                factors.append({
                    'factor': sensor_type,
                    'contribution_score': analysis['contribution_score'],
                    'risk_level': analysis['risk_level'],
                    'current_value': analysis['current_value'],
                    'description': self._get_factor_description(sensor_type, analysis)
                })
        
        return factors[:5]  # Return top 5 factors
    
    def _get_factor_description(self, sensor_type: str, analysis: Dict) -> str:
        """Generate human-readable description for a risk factor"""
        descriptions = {
            'vibration': f"Ground vibration at {analysis['current_value']:.1f} Hz indicates structural instability",
            'temperature': f"Temperature of {analysis['current_value']:.1f}°C affects rock thermal expansion",
            'humidity': f"Humidity at {analysis['current_value']:.1f}% impacts rock moisture content",
            'pressure': f"Atmospheric pressure of {analysis['current_value']:.1f} hPa affects rock stress",
            'acoustic': f"Acoustic emissions at {analysis['current_value']:.1f} dB indicate rock stress",
            'slope_stability': f"Slope stability factor of {analysis['current_value']:.2f} shows geological risk"
        }
        
        return descriptions.get(sensor_type, f"{sensor_type} reading of {analysis['current_value']}")
    
    def _check_threshold_violations(self, sensor_data: Dict) -> List[Dict]:
        """Check which sensors have exceeded critical thresholds"""
        violations = []
        
        for sensor_type, value in sensor_data.items():
            if sensor_type in self.risk_thresholds:
                thresholds = self.risk_thresholds[sensor_type]
                
                # Check for violations
                if value >= thresholds.get('critical', {}).get('min', float('inf')):
                    severity = 'CRITICAL'
                    threshold = thresholds['critical']['min']
                elif value >= thresholds.get('high', {}).get('min', float('inf')):
                    severity = 'HIGH'
                    threshold = thresholds['high']['min']
                elif value >= thresholds.get('medium', {}).get('min', float('inf')):
                    severity = 'MEDIUM'
                    threshold = thresholds['medium']['min']
                else:
                    continue  # No violation
                
                violations.append({
                    'sensor_type': sensor_type,
                    'current_value': value,
                    'threshold_value': threshold,
                    'excess_amount': value - threshold,
                    'severity': severity,
                    'percentage_over': ((value - threshold) / threshold * 100) if threshold > 0 else 0
                })
        
        return sorted(violations, key=lambda x: x['excess_amount'], reverse=True)
    
    def _analyze_trends(self, current_data: Dict, historical_data: List) -> Dict:
        """Analyze trends in sensor data over time"""
        if not historical_data or len(historical_data) < 2:
            return None
        
        trends = {}
        
        for sensor_type in current_data:
            historical_values = [d.get(sensor_type) for d in historical_data if d.get(sensor_type) is not None]
            
            if len(historical_values) >= 2:
                # Calculate trend
                recent_avg = sum(historical_values[-3:]) / len(historical_values[-3:])
                older_avg = sum(historical_values[:3]) / len(historical_values[:3])
                
                trend_direction = 'increasing' if recent_avg > older_avg else 'decreasing' if recent_avg < older_avg else 'stable'
                trend_rate = abs(recent_avg - older_avg) / older_avg * 100 if older_avg != 0 else 0
                
                trends[sensor_type] = {
                    'direction': trend_direction,
                    'rate_of_change': trend_rate,
                    'recent_average': recent_avg,
                    'historical_average': older_avg,
                    'volatility': self._calculate_volatility(historical_values)
                }
        
        return trends
    
    def _calculate_volatility(self, values: List[float]) -> float:
        """Calculate volatility (standard deviation) of sensor readings"""
        if len(values) < 2:
            return 0
        
        mean_value = sum(values) / len(values)
        variance = sum((x - mean_value) ** 2 for x in values) / len(values)
        return variance ** 0.5
    
    def _generate_explanation_narrative(self, sensor_analysis: Dict, primary_factors: List, 
                                      violations: List, alert_level: str) -> str:
        """Generate human-readable explanation narrative"""
        
        if alert_level == 'HIGH':
            explanation = "⚠️ HIGH RISK DETECTED: "
        elif alert_level == 'MEDIUM':
            explanation = "⚠️ MEDIUM RISK DETECTED: "
        else:
            explanation = "ℹ️ LOW RISK STATUS: "
        
        if violations:
            critical_violations = [v for v in violations if v['severity'] == 'CRITICAL']
            high_violations = [v for v in violations if v['severity'] == 'HIGH']
            
            if critical_violations:
                violation = critical_violations[0]
                explanation += f"CRITICAL threshold exceeded for {violation['sensor_type']} "
                explanation += f"({violation['current_value']:.1f} vs threshold {violation['threshold_value']:.1f}). "
            elif high_violations:
                violation = high_violations[0]
                explanation += f"High threshold exceeded for {violation['sensor_type']} "
                explanation += f"({violation['current_value']:.1f} vs threshold {violation['threshold_value']:.1f}). "
        
        # Add primary contributing factors
        if primary_factors:
            explanation += "Primary risk contributors: "
            factor_names = [f"{factor['factor']} ({factor['risk_level']} level)" for factor in primary_factors[:3]]
            explanation += ", ".join(factor_names) + ". "
        
        # Add specific recommendations based on alert level
        if alert_level == 'HIGH':
            explanation += "Immediate evacuation recommended due to imminent rockfall danger."
        elif alert_level == 'MEDIUM':
            explanation += "Enhanced monitoring and restricted access advised."
        else:
            explanation += "Continue standard safety protocols with regular monitoring."
        
        return explanation
    
    def _generate_recommendations(self, primary_factors: List, violations: List, alert_level: str) -> List[str]:
        """Generate actionable recommendations based on risk analysis"""
        recommendations = []
        
        # Alert-level specific recommendations
        if alert_level == 'HIGH':
            recommendations.extend([
                "🚨 IMMEDIATE EVACUATION: Remove all personnel from danger zones",
                "🛑 STOP OPERATIONS: Halt all mining activities immediately",
                "📞 EMERGENCY PROTOCOL: Activate emergency response procedures",
                "👥 PERSONNEL COUNT: Verify all workers are accounted for"
            ])
        elif alert_level == 'MEDIUM':
            recommendations.extend([
                "⚠️ RESTRICT ACCESS: Limit personnel in high-risk areas",
                "📈 INCREASE MONITORING: Enhance sensor monitoring frequency",
                "📋 SAFETY BRIEFING: Brief all personnel on current risk status",
                "🚧 PREPARE EVACUATION: Ready evacuation procedures if needed"
            ])
        
        # Factor-specific recommendations
        for factor in primary_factors:
            sensor_type = factor['factor']
            if sensor_type == 'vibration' and factor['risk_level'] in ['high', 'critical']:
                recommendations.append(f"🔍 VIBRATION CHECK: Inspect for structural instability - reading at {factor['current_value']:.1f} Hz")
            elif sensor_type == 'acoustic' and factor['risk_level'] in ['high', 'critical']:
                recommendations.append(f"👂 ACOUSTIC MONITORING: Investigate sound sources - emissions at {factor['current_value']:.1f} dB")
            elif sensor_type == 'slope_stability' and factor['risk_level'] in ['high', 'critical']:
                recommendations.append(f"🏔️ GEOLOGICAL ASSESSMENT: Conduct slope stability analysis - factor at {factor['current_value']:.2f}")
            elif sensor_type == 'temperature' and factor['risk_level'] in ['high', 'critical']:
                recommendations.append(f"🌡️ THERMAL MONITORING: Check for thermal expansion effects - temp at {factor['current_value']:.1f}°C")
        
        # Violation-specific recommendations
        for violation in violations[:2]:  # Top 2 violations
            if violation['severity'] == 'CRITICAL':
                recommendations.append(f"🔴 CRITICAL ALERT: {violation['sensor_type'].title()} at {violation['current_value']:.1f} - {violation['percentage_over']:.1f}% over threshold")
        
        return recommendations[:8]  # Limit to most important recommendations
    
    def _calculate_confidence(self, sensor_analysis: Dict) -> float:
        """Calculate confidence level in risk assessment (0-100%)"""
        if not sensor_analysis:
            return 50.0  # Default confidence
        
        # Factors that increase confidence:
        # 1. More sensors providing data
        # 2. Consistent risk levels across sensors
        # 3. Clear threshold violations
        
        sensor_count = len(sensor_analysis)
        sensor_weight = min(100.0, sensor_count * 15)  # Up to 100% for 7+ sensors
        
        # Check consistency of risk levels
        risk_levels = [s['risk_level'] for s in sensor_analysis.values()]
        high_risk_count = sum(1 for level in risk_levels if level in ['high', 'critical'])
        consistency_weight = (high_risk_count / len(risk_levels)) * 50 if risk_levels else 0
        
        confidence = min(100.0, sensor_weight + consistency_weight)
        return round(confidence, 1)
    
    def get_multilingual_explanations(self, explanation_dict: Dict, languages: List[str]) -> Dict:
        """Generate risk explanations in multiple languages"""
        multilingual_explanations = {}
        
        translations = self._get_explanation_translations()
        
        for lang in languages:
            if lang in translations:
                lang_explanation = self._translate_explanation(explanation_dict, translations[lang])
                multilingual_explanations[lang] = lang_explanation
        
        return multilingual_explanations
    
    def _get_explanation_translations(self) -> Dict:
        """Get translation mappings for risk explanations"""
        return {
            'english': {
                'high_risk': 'HIGH RISK DETECTED',
                'medium_risk': 'MEDIUM RISK DETECTED', 
                'low_risk': 'LOW RISK STATUS',
                'primary_contributors': 'Primary risk contributors',
                'vibration': 'ground vibration',
                'temperature': 'temperature',
                'humidity': 'humidity',
                'pressure': 'atmospheric pressure',
                'acoustic': 'acoustic emissions',
                'slope_stability': 'slope stability',
                'threshold_exceeded': 'threshold exceeded',
                'immediate_evacuation': 'Immediate evacuation recommended',
                'enhanced_monitoring': 'Enhanced monitoring advised'
            },
            'hindi': {
                'high_risk': 'उच्च जोखिम का पता चला',
                'medium_risk': 'मध्यम जोखिम का पता चला',
                'low_risk': 'कम जोखिम की स्थिति',
                'primary_contributors': 'मुख्य जोखिम कारक',
                'vibration': 'भूकंपन',
                'temperature': 'तापमान',
                'humidity': 'नमी',
                'pressure': 'वायुमंडलीय दबाव',
                'acoustic': 'ध्वनि उत्सर्जन',
                'slope_stability': 'ढलान स्थिरता',
                'threshold_exceeded': 'सीमा पार हो गई',
                'immediate_evacuation': 'तत्काल निकासी की सिफारिश',
                'enhanced_monitoring': 'बेहतर निगरानी की सलाह'
            }
            # Additional language translations can be added here
        }
    
    def _translate_explanation(self, explanation_dict: Dict, translations: Dict) -> str:
        """Translate explanation to specified language"""
        # This is a simplified translation - in production, use proper translation service
        alert_level = explanation_dict['alert_level']
        
        if alert_level == 'HIGH':
            base_text = translations.get('high_risk', 'HIGH RISK DETECTED')
        elif alert_level == 'MEDIUM':
            base_text = translations.get('medium_risk', 'MEDIUM RISK DETECTED')
        else:
            base_text = translations.get('low_risk', 'LOW RISK STATUS')
        
        return base_text + ": " + explanation_dict.get('primary_explanation', '')


def create_sample_explanation():
    """Create a sample risk explanation for testing"""
    explainer = RockfallRiskExplainer()
    
    sample_sensor_data = {
        'vibration': 8.2,
        'temperature': 45.3,
        'humidity': 89.1,
        'pressure': 1015.2,
        'acoustic': 95.7,
        'slope_stability': 0.42
    }
    
    explanation = explainer.explain_risk_assessment(
        sensor_data=sample_sensor_data,
        risk_score=8.7,
        alert_level='HIGH'
    )
    
    return explanation


if __name__ == "__main__":
    # Test the explanation system
    sample_explanation = create_sample_explanation()
    print("Sample Risk Explanation:")
    print("=" * 60)
    print(json.dumps(sample_explanation, indent=2, ensure_ascii=False))
