import pickle
import numpy as np
import pandas as pd
import os
from datetime import datetime
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class RockfallPredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.load_models()
        
    def load_models(self):
        """Load the trained ML models"""
        try:
            # ======== CHANGED: Load LightGBM model ========
            model_path = os.path.join('output', 'best_rockfall_model.joblib')
            if os.path.exists(model_path):
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                    print("Loaded LightGBM model successfully")
            else:
                print("Warning: LightGBM model not found. Using fallback logic.")

            # Load scaler
            scaler_path = os.path.join('output', 'scaler.joblib')
            if os.path.exists(scaler_path):
                with open(scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)

            # Load selected features
            feature_path = os.path.join('output', 'selected_features.pkl')
            if os.path.exists(feature_path):
                with open(feature_path, 'rb') as f:
                    self.feature_columns = pickle.load(f)

        except Exception as e:
            print(f"Error loading models: {e}")
    
    def prepare_features(self, mine_data):
        features = {}

        features['elevation'] = mine_data.get('elevation', 1000)
        features['slope'] = mine_data.get('slope', 25)
        features['aspect'] = mine_data.get('aspect', 180)
        features['latitude_x'] = mine_data.get('latitude', 20.0)
        features['longitude_x'] = mine_data.get('longitude', 77.0)

        features['depth'] = mine_data.get('earthquake_depth', 10)
        features['mag'] = mine_data.get('earthquake_magnitude', 2.5)
        features['nst'] = mine_data.get('earthquake_nst', 15)
        features['gap'] = mine_data.get('earthquake_gap', 180)
        features['dmin'] = mine_data.get('earthquake_dmin', 0.5)
        features['rms'] = mine_data.get('earthquake_rms', 0.1)
        features['horizontalError'] = mine_data.get('earthquake_horizontal_error', 1.0)
        features['depthError'] = mine_data.get('earthquake_depth_error', 2.0)
        features['magError'] = mine_data.get('earthquake_mag_error', 0.1)
        features['magNst'] = mine_data.get('earthquake_mag_nst', 10)

        features['JAN'] = mine_data.get('rainfall_jan', 15)
        features['FEB'] = mine_data.get('rainfall_feb', 20)
        features['MAR'] = mine_data.get('rainfall_mar', 25)
        features['APR'] = mine_data.get('rainfall_apr', 30)
        features['MAY'] = mine_data.get('rainfall_may', 40)
        features['JUN'] = mine_data.get('rainfall_jun', 100)
        features['JUL'] = mine_data.get('rainfall_jul', 150)
        features['AUG'] = mine_data.get('rainfall_aug', 140)
        features['SEP'] = mine_data.get('rainfall_sep', 120)
        features['OCT'] = mine_data.get('rainfall_oct', 60)
        features['NOV'] = mine_data.get('rainfall_nov', 25)
        features['DEC'] = mine_data.get('rainfall_dec', 10)

        features['ANNUAL'] = sum(features[m] for m in
                                 ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'])

        features['Jan-Feb'] = features['JAN'] + features['FEB']
        features['Mar-May'] = features['MAR'] + features['APR'] + features['MAY']
        features['Jun-Sep'] = features['JUN'] + features['JUL'] + features['AUG'] + features['SEP']
        features['Oct-Dec'] = features['OCT'] + features['NOV'] + features['DEC']

        features['Displacement_mm'] = mine_data.get('displacement', 2.0)
        features['Strain_micro'] = mine_data.get('strain', 50)
        features['PorePressure_kPa'] = mine_data.get('pore_pressure', 100)
        features['SeismicVibration_mm/s'] = mine_data.get('seismic_vibration', 5.0)

        features['drone_id'] = mine_data.get('drone_id', 1)
        features['crack_density'] = mine_data.get('crack_density', 0.03)
        features['debris_entropy'] = mine_data.get('debris_entropy', 3.5)
        features['debris_contrast'] = mine_data.get('debris_contrast', 400)
        features['debris_homogeneity'] = mine_data.get('debris_homogeneity', 0.6)
        features['vegetation_green_ratio'] = mine_data.get('vegetation_ratio', 0.4)

        current_time = datetime.now()
        features['year'] = current_time.year
        features['month'] = current_time.month
        features['day'] = current_time.day
        features['season'] = self.get_season(current_time.month)

        features['SUBDIVISION'] = mine_data.get('subdivision', 'JHARKHAND')

        return features
    
    def get_season(self, month):
        if month in [12, 1, 2]:
            return 0
        elif month in [3, 4, 5]:
            return 1
        elif month in [6, 7, 8, 9]:
            return 2
        else:
            return 3
    
    def predict_risk(self, mine_data):
        """Predict rockfall risk using LightGBM model (fallback preserved)"""
        try:
            features = self.prepare_features(mine_data)
            df = pd.DataFrame([features])

            df["SUBDIVISION"] = df["SUBDIVISION"].astype("category").cat.codes

            if self.feature_columns:
                df = df[self.feature_columns]

            if self.scaler:
                df = self.scaler.transform(df)

            # ======== CHANGED: Actual model prediction ========
            if self.model:
                probs = self.model.predict_proba(df)[0]
                risk_class = int(np.argmax(probs))
                risk_score = float(probs[2])
                risk_level = ["LOW", "MEDIUM", "HIGH"][risk_class]
                confidence = float(np.max(probs))
            else:
                risk_score, risk_level = self._calculate_geological_risk(mine_data)
                confidence = 0.5

            key_factors = self.generate_realistic_factors(risk_score, features, mine_data)

            return {
                'risk_level': risk_level,
                'risk_score': float(risk_score),
                'confidence': float(confidence),
                'key_factors': key_factors,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            print("Prediction error:", e)
            return {
                'risk_level': 'LOW',
                'risk_score': 0.1,
                'confidence': 0.5,
                'key_factors': ['Fallback used'],
                'timestamp': datetime.now().isoformat()
            }

    # ======= EVERYTHING BELOW IS 100% UNCHANGED =======
    # calculate_fallback_risk
    # categorize_risk
    # identify_key_factors
    # generate_realistic_factors
    # _calculate_geological_risk
    # _generate_realistic_sensor_data
