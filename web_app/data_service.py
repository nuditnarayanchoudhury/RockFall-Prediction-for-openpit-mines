import json
import random
import numpy as np
from datetime import datetime, timedelta
import requests
import time
try:
    from sentinel1_service import Sentinel1DataService
except ImportError:
    Sentinel1DataService = None

class DataService:
    def __init__(self):
        self.indian_mines = self.load_indian_mines()
        # Initialize Sentinel-1 service for real SAR data
        self.sentinel1_service = Sentinel1DataService() if Sentinel1DataService else None
        
    def load_indian_mines(self):
        """Load comprehensive database of Indian open-pit mines"""
        mines = [
            # JHARKHAND - Coal Mining Hub
            {
                'id': 'mine_001',
                'name': 'Jharia Coalfield',
                'type': 'Coal',
                'location': 'Dhanbad, Jharkhand',
                'coordinates': [23.7644, 86.4084],
                'state': 'JHARKHAND',
                'operator': 'Bharat Coking Coal Limited (BCCL)',
                'area_km2': 450,
                'depth_m': 200,
                'status': 'Active',
                'risk_factors': ['Underground fires', 'Subsidence', 'High rainfall']
            },
            {
                'id': 'mine_002',
                'name': 'Bokaro Coalfield',
                'type': 'Coal',
                'location': 'Bokaro, Jharkhand',
                'coordinates': [23.7907, 85.9618],
                'state': 'JHARKHAND',
                'operator': 'Coal India Limited',
                'area_km2': 220,
                'depth_m': 150,
                'status': 'Active',
                'risk_factors': ['Slope stability', 'Groundwater']
            },
            {
                'id': 'mine_003',
                'name': 'Rajmahal Coalfield',
                'type': 'Coal',
                'location': 'Sahebganj, Jharkhand',
                'coordinates': [25.2425, 87.6188],
                'state': 'JHARKHAND',
                'operator': 'Eastern Coalfields Limited (ECL)',
                'area_km2': 1500,
                'depth_m': 180,
                'status': 'Active',
                'risk_factors': ['Seismic activity', 'River proximity']
            },
            
            # ODISHA - Major Mining State
            {
                'id': 'mine_004',
                'name': 'Keonjhar Iron Ore Mines',
                'type': 'Iron Ore',
                'location': 'Keonjhar, Odisha',
                'coordinates': [21.6297, 85.5804],
                'state': 'ODISHA',
                'operator': 'Odisha Mining Corporation',
                'area_km2': 300,
                'depth_m': 250,
                'status': 'Active',
                'risk_factors': ['High grade slopes', 'Monsoon impact']
            },
            {
                'id': 'mine_005',
                'name': 'Barbil Iron Ore Complex',
                'type': 'Iron Ore',
                'location': 'Barbil, Keonjhar, Odisha',
                'coordinates': [22.1167, 85.3833],
                'state': 'ODISHA',
                'operator': 'Tata Steel',
                'area_km2': 180,
                'depth_m': 300,
                'status': 'Active',
                'risk_factors': ['Deep excavation', 'Rock weathering']
            },
            {
                'id': 'mine_006',
                'name': 'Talcher Coalfield',
                'type': 'Coal',
                'location': 'Angul, Odisha',
                'coordinates': [20.9513, 85.2266],
                'state': 'ODISHA',
                'operator': 'Mahanadi Coalfields Limited (MCL)',
                'area_km2': 600,
                'depth_m': 200,
                'status': 'Active',
                'risk_factors': ['Groundwater', 'Overburden stability']
            },
            
            # CHHATTISGARH - Coal Rich Region
            {
                'id': 'mine_007',
                'name': 'Korba Coalfield',
                'type': 'Coal',
                'location': 'Korba, Chhattisgarh',
                'coordinates': [22.3595, 82.7501],
                'state': 'CHHATTISGARH',
                'operator': 'South Eastern Coalfields Limited (SECL)',
                'area_km2': 1200,
                'depth_m': 180,
                'status': 'Active',
                'risk_factors': ['Highwall stability', 'Dust storms']
            },
            {
                'id': 'mine_008',
                'name': 'Raigarh Coalfield',
                'type': 'Coal',
                'location': 'Raigarh, Chhattisgarh',
                'coordinates': [21.8974, 83.3953],
                'state': 'CHHATTISGARH',
                'operator': 'Coal India Limited',
                'area_km2': 500,
                'depth_m': 220,
                'status': 'Active',
                'risk_factors': ['Slope failure', 'Forest clearance']
            },
            
            # RAJASTHAN - Minerals Mining
            {
                'id': 'mine_009',
                'name': 'Zawar Mines',
                'type': 'Lead-Zinc',
                'location': 'Udaipur, Rajasthan',
                'coordinates': [24.3006, 73.8553],
                'state': 'RAJASTHAN',
                'operator': 'Hindustan Zinc Limited',
                'area_km2': 80,
                'depth_m': 400,
                'status': 'Active',
                'risk_factors': ['Deep shafts', 'Water ingress', 'Desert climate']
            },
            {
                'id': 'mine_010',
                'name': 'Rampura Agucha Mine',
                'type': 'Lead-Zinc',
                'location': 'Bhilwara, Rajasthan',
                'coordinates': [25.2138, 74.7734],
                'state': 'RAJASTHAN',
                'operator': 'Hindustan Zinc Limited',
                'area_km2': 120,
                'depth_m': 350,
                'status': 'Active',
                'risk_factors': ['High-grade ore body', 'Rock bursts']
            },
            
            # GUJARAT - Lignite Mining
            {
                'id': 'mine_011',
                'name': 'Kutch Lignite Mines',
                'type': 'Lignite',
                'location': 'Kutch, Gujarat',
                'coordinates': [23.2156, 69.6691],
                'state': 'GUJARAT',
                'operator': 'Gujarat Mineral Development Corporation',
                'area_km2': 400,
                'depth_m': 100,
                'status': 'Active',
                'risk_factors': ['Soft overburden', 'Saline water']
            },
            
            # WEST BENGAL
            {
                'id': 'mine_012',
                'name': 'Raniganj Coalfield',
                'type': 'Coal',
                'location': 'Paschim Bardhaman, West Bengal',
                'coordinates': [23.6223, 87.1265],
                'state': 'WEST BENGAL',
                'operator': 'Eastern Coalfields Limited',
                'area_km2': 1500,
                'depth_m': 150,
                'status': 'Active',
                'risk_factors': ['Underground workings', 'Subsidence']
            },
            
            # MAHARASHTRA
            {
                'id': 'mine_013',
                'name': 'Chandrapur Coal Mines',
                'type': 'Coal',
                'location': 'Chandrapur, Maharashtra',
                'coordinates': [19.9615, 79.2961],
                'state': 'MAHARASHTRA',
                'operator': 'Western Coalfields Limited (WCL)',
                'area_km2': 800,
                'depth_m': 160,
                'status': 'Active',
                'risk_factors': ['Basaltic terrain', 'Water table']
            },
            
            # KARNATAKA - Iron Ore
            {
                'id': 'mine_014',
                'name': 'Bellary Iron Ore Mines',
                'type': 'Iron Ore',
                'location': 'Bellary, Karnataka',
                'coordinates': [15.1394, 76.9214],
                'state': 'KARNATAKA',
                'operator': 'NMDC Limited',
                'area_km2': 200,
                'depth_m': 200,
                'status': 'Active',
                'risk_factors': ['Hard rock mining', 'Slope stability']
            },
            
            # TELANGANA
            {
                'id': 'mine_015',
                'name': 'Singareni Coalfields',
                'type': 'Coal',
                'location': 'Godavarikhani, Telangana',
                'coordinates': [18.7465, 79.4981],
                'state': 'TELANGANA',
                'operator': 'Singareni Collieries Company Limited (SCCL)',
                'area_km2': 350,
                'depth_m': 180,
                'status': 'Active',
                'risk_factors': ['Gas emissions', 'Fault zones']
            },
            
            # ANDHRA PRADESH
            {
                'id': 'mine_016',
                'name': 'Cuddapah Limestone Quarries',
                'type': 'Limestone',
                'location': 'Cuddapah, Andhra Pradesh',
                'coordinates': [14.4673, 78.8242],
                'state': 'ANDHRA PRADESH',
                'operator': 'Multiple Private Operators',
                'area_km2': 150,
                'depth_m': 120,
                'status': 'Active',
                'risk_factors': ['Karst geology', 'Water ingress']
            },
            
            # MADHYA PRADESH
            {
                'id': 'mine_017',
                'name': 'Panna Diamond Mines',
                'type': 'Diamond',
                'location': 'Panna, Madhya Pradesh',
                'coordinates': [24.7192, 80.1919],
                'state': 'MADHYA PRADESH',
                'operator': 'National Mineral Development Corporation',
                'area_km2': 60,
                'depth_m': 200,
                'status': 'Active',
                'risk_factors': ['Kimberlite pipes', 'Precise extraction required']
            },
            {
                'id': 'mine_018',
                'name': 'Satpura Coalfield',
                'type': 'Coal',
                'location': 'Betul, Madhya Pradesh',
                'coordinates': [21.9077, 77.8980],
                'state': 'MADHYA PRADESH',
                'operator': 'Western Coalfields Limited',
                'area_km2': 400,
                'depth_m': 170,
                'status': 'Active',
                'risk_factors': ['Hilly terrain', 'Forest area']
            }
        ]
        
        return mines
    
    def get_indian_mines(self):
        """Return list of all Indian open-pit mines"""
        return self.indian_mines
    
    def get_mine_by_id(self, mine_id):
        """Get specific mine by ID"""
        for mine in self.indian_mines:
            if mine['id'] == mine_id:
                return mine
        return None
    
    def get_realtime_data(self, mine_id):
        """Simulate real-time data for a specific mine"""
        mine = self.get_mine_by_id(mine_id)
        if not mine:
            return {}
        
        # Base parameters based on mine characteristics
        base_seismic = self.get_base_seismic_activity(mine)
        base_rainfall = self.get_seasonal_rainfall(mine)
        
        # Generate realistic real-time data with some randomness
        current_time = datetime.now()
        
        # Get Sentinel-1 SAR data if available
        sar_features = {}
        if self.sentinel1_service:
            try:
                sar_data = self.sentinel1_service.extract_sar_features(
                    mine['coordinates'], 
                    {'subdivision': mine['state'], 'slope': random.uniform(15, 50)}
                )
                sar_features = sar_data
            except Exception as e:
                print(f"Warning: Could not fetch Sentinel-1 data for {mine['name']}: {e}")
        
        base_data = {
            # Geospatial data from mine properties
            'latitude': mine['coordinates'][0] + random.uniform(-0.01, 0.01),
            'longitude': mine['coordinates'][1] + random.uniform(-0.01, 0.01),
            'elevation': random.uniform(200, 1500),
            'slope': random.uniform(15, 50),  # Typical open-pit slopes
            'aspect': random.uniform(0, 360),
            
            # Earthquake/Seismic data
            'earthquake_depth': random.uniform(5, 30),
            'earthquake_magnitude': base_seismic + random.uniform(-0.5, 1.0),
            'earthquake_nst': random.randint(8, 25),
            'earthquake_gap': random.uniform(50, 300),
            'earthquake_dmin': random.uniform(0.1, 2.0),
            'earthquake_rms': random.uniform(0.05, 0.3),
            'earthquake_horizontal_error': random.uniform(0.5, 3.0),
            'earthquake_depth_error': random.uniform(1.0, 5.0),
            'earthquake_mag_error': random.uniform(0.05, 0.2),
            'earthquake_mag_nst': random.randint(5, 20),
            
            # Current weather-based rainfall
            'rainfall_jan': base_rainfall['jan'] + random.uniform(-10, 10),
            'rainfall_feb': base_rainfall['feb'] + random.uniform(-10, 10),
            'rainfall_mar': base_rainfall['mar'] + random.uniform(-10, 10),
            'rainfall_apr': base_rainfall['apr'] + random.uniform(-15, 15),
            'rainfall_may': base_rainfall['may'] + random.uniform(-20, 20),
            'rainfall_jun': base_rainfall['jun'] + random.uniform(-30, 50),
            'rainfall_jul': base_rainfall['jul'] + random.uniform(-40, 60),
            'rainfall_aug': base_rainfall['aug'] + random.uniform(-40, 60),
            'rainfall_sep': base_rainfall['sep'] + random.uniform(-30, 50),
            'rainfall_oct': base_rainfall['oct'] + random.uniform(-20, 20),
            'rainfall_nov': base_rainfall['nov'] + random.uniform(-10, 10),
            'rainfall_dec': base_rainfall['dec'] + random.uniform(-10, 10),
            
            # Geotechnical sensor data - realistic for mining operations
            'displacement': self.generate_displacement_reading(mine),
            'strain': self.generate_strain_reading(mine),
            'pore_pressure': self.generate_pore_pressure_reading(mine),
            'seismic_vibration': self.generate_seismic_vibration(mine, base_seismic),
            
            # Drone-derived features with realistic variations
            'drone_id': random.randint(1, 10),
            'crack_density': self.generate_crack_density(mine),
            'debris_entropy': random.uniform(1.0, 7.0),
            'debris_contrast': random.uniform(50, 1000),
            'debris_homogeneity': random.uniform(0.1, 0.98),
            'vegetation_ratio': self.generate_vegetation_ratio(mine),
            
        # Mine-specific data
        'subdivision': mine['state'],
        'mine_type': mine['type'],
        'depth': mine['depth_m'],
        'area': mine['area_km2'],
        'mine_name': mine['name'],
        'mine_id': mine['id'],
            
            # Timestamp
            'timestamp': current_time.isoformat()
        }
        
        # Merge Sentinel-1 SAR features if available
        if sar_features:
            # Add SAR-derived features that are relevant for rockfall prediction
            base_data.update({
                # SAR displacement features (convert to match existing features)
                'sar_displacement_mm': sar_features.get('los_displacement_mm', 0),
                'sar_displacement_velocity': sar_features.get('displacement_velocity_mm_month', 0),
                'sar_coherence': sar_features.get('coherence_vv', 0.5),
                'sar_backscatter_vv': sar_features.get('backscatter_vv_db', -12),
                'sar_backscatter_vh': sar_features.get('backscatter_vh_db', -18),
                'sar_surface_deformation_rate': sar_features.get('surface_deformation_rate', 0),
                'sar_temporal_decorrelation': sar_features.get('temporal_decorrelation', 0.2),
                'sar_data_quality': sar_features.get('data_quality_score', 0.7),
                
                # Enhanced displacement reading using SAR data
                'displacement': max(
                    self.generate_displacement_reading(mine),
                    abs(sar_features.get('los_displacement_mm', 0))
                ),
                
                # Enhanced crack density using SAR coherence loss
                'crack_density': max(
                    self.generate_crack_density(mine),
                    sar_features.get('temporal_decorrelation', 0) * 0.1
                ),
                
                # Metadata
                'sar_acquisition_date': sar_features.get('acquisition_date'),
                'sar_data_source': 'Sentinel-1' if not sar_features.get('synthetic_data', True) else 'Synthetic SAR'
            })
        
        return base_data
    
    def get_base_seismic_activity(self, mine):
        """Get base seismic activity level for mine location"""
        seismic_zones = {
            'JHARKHAND': 2.8,  # Moderate seismic zone
            'ODISHA': 2.5,
            'CHHATTISGARH': 2.2,
            'WEST BENGAL': 3.0,  # Higher due to tectonic activity
            'RAJASTHAN': 2.0,    # Lower seismic activity
            'GUJARAT': 3.5,      # High due to Arabian Sea plate
            'MAHARASHTRA': 2.8,
            'KARNATAKA': 2.3,
            'TELANGANA': 2.1,
            'ANDHRA PRADESH': 2.4,
            'MADHYA PRADESH': 2.0
        }
        return seismic_zones.get(mine['state'], 2.5)
    
    def get_seasonal_rainfall(self, mine):
        """Get seasonal rainfall pattern based on mine location"""
        # Monsoon patterns vary by region
        monsoon_intensity = {
            'JHARKHAND': 1.2,
            'ODISHA': 1.4,     # Higher monsoon impact
            'CHHATTISGARH': 1.1,
            'WEST BENGAL': 1.5,  # Very high monsoon
            'RAJASTHAN': 0.3,    # Desert - low rainfall
            'GUJARAT': 0.8,
            'MAHARASHTRA': 1.0,
            'KARNATAKA': 0.9,
            'TELANGANA': 0.8,
            'ANDHRA PRADESH': 0.9,
            'MADHYA PRADESH': 0.9
        }
        
        intensity = monsoon_intensity.get(mine['state'], 1.0)
        
        return {
            'jan': 15 * intensity,
            'feb': 20 * intensity,
            'mar': 25 * intensity,
            'apr': 30 * intensity,
            'may': 45 * intensity,
            'jun': 120 * intensity,
            'jul': 180 * intensity,
            'aug': 160 * intensity,
            'sep': 140 * intensity,
            'oct': 80 * intensity,
            'nov': 30 * intensity,
            'dec': 15 * intensity
        }
    
    def generate_displacement_reading(self, mine):
        """Generate realistic displacement readings with dynamic risk scenarios"""
        # Higher displacement in deeper mines and certain rock types
        base_displacement = mine['depth_m'] / 100  # Base on depth
        
        # Add mine type factor
        type_factors = {
            'Coal': 1.5,      # Coal mines have more displacement
            'Iron Ore': 1.0,  # Stable rock
            'Limestone': 1.2,
            'Lead-Zinc': 0.8,
            'Diamond': 0.6,   # Very stable extraction
            'Lignite': 2.0    # Soft material, high displacement
        }
        
        factor = type_factors.get(mine['type'], 1.0)
        displacement = base_displacement * factor + random.uniform(-1, 3)
        
        # Time-based risk cycles (some mines have higher risk periods)
        current_time = datetime.now()
        time_based_multiplier = 1.0
        
        # Create rotating high-risk periods based on mine ID and time
        mine_hash = hash(mine['id']) % 24  # 24-hour cycle
        current_hour = current_time.hour
        
        # Each mine has a 6-hour high risk window in 24 hours
        if (current_hour >= mine_hash and current_hour < (mine_hash + 6)) or \
           (mine_hash > 18 and current_hour < (mine_hash + 6 - 24)):
            time_based_multiplier += 1.5  # 150% increase during risk period
        
        # Create realistic high-risk displacement scenarios based on mine characteristics
        mine_risk_factors = mine.get('risk_factors', [])
        displacement_risk_chance = 0.20  # Increased base chance to 20%
        
        # Higher risk for certain mine types and risk factors
        if mine['type'] in ['Coal'] and 'Underground fires' in mine_risk_factors:
            displacement_risk_chance += 0.45  # Coal mines with fires are very risky
        elif 'Deep excavation' in mine_risk_factors or 'High grade slopes' in mine_risk_factors:
            displacement_risk_chance += 0.35
        elif 'Slope stability' in mine_risk_factors:
            displacement_risk_chance += 0.30
        
        # Day-based risk variation (some days are riskier)
        day_risk_multiplier = 1.0
        day_of_year = current_time.timetuple().tm_yday
        mine_day_hash = (hash(mine['id']) + day_of_year) % 7
        if mine_day_hash < 2:  # 2 out of 7 days are higher risk
            day_risk_multiplier = 2.0
            displacement_risk_chance += 0.25
        
        displacement *= time_based_multiplier * day_risk_multiplier
        
        if random.random() < displacement_risk_chance:
            displacement += random.uniform(6, 15)  # Dangerous displacement levels
            
        return max(0.1, displacement)  # Ensure positive
    
    def generate_strain_reading(self, mine):
        """Generate realistic strain readings (micro-strain)"""
        base_strain = random.uniform(20, 80)
        
        # Higher strain in certain conditions
        if 'High grade slopes' in mine.get('risk_factors', []):
            base_strain += 30
        if 'Deep excavation' in mine.get('risk_factors', []):
            base_strain += 40
            
        return base_strain + random.uniform(-10, 30)
    
    def generate_pore_pressure_reading(self, mine):
        """Generate realistic pore pressure readings"""
        base_pressure = random.uniform(80, 150)
        
        # Higher pressure in water-related risk areas
        if 'Groundwater' in mine.get('risk_factors', []):
            base_pressure += 50
        if 'Water ingress' in mine.get('risk_factors', []):
            base_pressure += 70
            
        return base_pressure + random.uniform(-20, 40)
    
    def generate_seismic_vibration(self, mine, base_seismic):
        """Generate seismic vibration readings with dynamic risk scenarios"""
        vibration = base_seismic * 2 + random.uniform(-2, 8)
        
        # Time-based seismic patterns
        current_time = datetime.now()
        
        # Some mines have higher seismic activity during certain hours
        mine_seismic_hash = hash(mine['id'] + 'seismic') % 24
        current_hour = current_time.hour
        
        # 4-hour high seismic activity window for each mine
        if (current_hour >= mine_seismic_hash and current_hour < (mine_seismic_hash + 4)) or \
           (mine_seismic_hash > 20 and current_hour < (mine_seismic_hash + 4 - 24)):
            vibration *= 2.2  # Significant increase during high activity period
        
        # Add mining-specific factors
        if mine['type'] == 'Coal' and 'Underground fires' in mine.get('risk_factors', []):
            vibration += 5  # Fire-related instability (increased)
            
        # Weekly pattern - some mines are riskier on certain days
        day_of_week = current_time.weekday()
        mine_weekly_hash = hash(mine['id'] + 'weekly') % 7
        if day_of_week == mine_weekly_hash or day_of_week == (mine_weekly_hash + 3) % 7:
            vibration *= 1.8  # Higher risk on specific days
            
        # Create some high-risk scenarios based on mine characteristics
        # Certain mines are more prone to high risk based on their risk factors
        risk_prone_mines = ['Underground fires', 'Slope stability', 'High grade slopes', 
                           'Deep excavation', 'Rock weathering', 'Highwall stability']
        
        mine_risk_factors = mine.get('risk_factors', [])
        high_risk_probability = 0.30  # Increased base chance to 30%
        
        # Increase probability for mines with specific risk factors
        for risk_factor in risk_prone_mines:
            if risk_factor in mine_risk_factors:
                high_risk_probability += 0.35  # Increased from 0.25
        
        # Weather-based amplification (heavy rain increases seismic risk)
        month = current_time.month
        if month in [6, 7, 8, 9]:  # Monsoon months
            high_risk_probability += 0.15
            vibration *= 1.3
        
        # Create realistic risk scenarios
        if random.random() < high_risk_probability:
            vibration += random.uniform(10, 25)  # High risk vibration (increased)
            
        return max(0.5, vibration)
    
    def generate_crack_density(self, mine):
        """Generate crack density based on mine characteristics with dynamic patterns"""
        base_density = random.uniform(0.01, 0.06)
        
        # Time-based crack development patterns
        current_time = datetime.now()
        
        # Seasonal crack development (winter freezing/thawing increases cracks)
        month = current_time.month
        if month in [12, 1, 2, 3]:  # Winter and early spring
            base_density *= 1.4  # Freeze-thaw cycles increase cracking
        elif month in [6, 7, 8, 9]:  # Monsoon season
            base_density *= 1.3  # Water infiltration increases cracks
        
        # Daily crack progression patterns
        mine_crack_hash = hash(mine['id'] + 'cracks') % 30  # 30-day cycle
        day_of_month = current_time.day
        
        # Each mine has a 10-day high crack development period per month
        if (day_of_month >= mine_crack_hash and day_of_month < (mine_crack_hash + 10)) or \
           (mine_crack_hash > 20 and day_of_month < (mine_crack_hash + 10 - 30)):
            base_density *= 1.8  # Higher crack development during critical period
        
        # Higher crack density in problematic areas
        risk_factors = mine.get('risk_factors', [])
        if 'Slope stability' in risk_factors:
            base_density += 0.03  # Increased from 0.02
        if 'Rock weathering' in risk_factors:
            base_density += 0.025  # Increased from 0.015
        if 'Highwall stability' in risk_factors:
            base_density += 0.035  # Increased from 0.025
        if 'Underground fires' in risk_factors:
            base_density += 0.04  # Heat expansion causes cracks
            
        # Age-based crack accumulation (deeper mines are typically older)
        depth_factor = mine['depth_m'] / 500.0  # Normalize depth
        base_density += depth_factor * 0.02
        
        # Create high-risk scenarios based on mine-specific factors
        risk_multiplier = 1.0
        for risk_factor in risk_factors:
            if risk_factor in ['Slope stability', 'Rock weathering', 'Highwall stability']:
                risk_multiplier += 0.6  # Increased from 0.4
            elif risk_factor in ['Underground fires', 'Deep excavation']:
                risk_multiplier += 0.5  # Increased from 0.3
        
        # Generate realistic risk scenarios
        risk_chance = min(0.60, 0.15 * risk_multiplier)  # Increased from 40% cap and 0.1 multiplier
        if random.random() < risk_chance:
            base_density += random.uniform(0.04, 0.12)  # Dangerous crack levels (increased)
            
        return min(0.20, base_density)  # Increased cap to 0.20
    
    def generate_vegetation_ratio(self, mine):
        """Generate vegetation ratio based on location and season"""
        base_vegetation = random.uniform(0.1, 0.8)
        
        # Adjust based on state climate
        if mine['state'] in ['RAJASTHAN', 'GUJARAT']:
            base_vegetation *= 0.5  # Arid regions
        elif mine['state'] in ['WEST BENGAL', 'ODISHA']:
            base_vegetation *= 1.3  # High rainfall regions
            
        # Seasonal adjustment
        current_month = datetime.now().month
        if current_month in [6, 7, 8, 9]:  # Monsoon season
            base_vegetation *= 1.2
        elif current_month in [3, 4, 5]:   # Summer
            base_vegetation *= 0.8
            
        return min(0.95, base_vegetation)
    
    def get_historical_trends(self, mine_id, days=7):
        """Generate historical trend data for the past N days"""
        mine = self.get_mine_by_id(mine_id)
        if not mine:
            return []
            
        trends = []
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            
            # Generate data point for this date
            data_point = {
                'date': date.strftime('%Y-%m-%d'),
                'risk_score': random.uniform(0.1, 0.9),
                'displacement': self.generate_displacement_reading(mine),
                'seismic_vibration': self.generate_seismic_vibration(mine, self.get_base_seismic_activity(mine)),
                'crack_density': self.generate_crack_density(mine),
                'rainfall': random.uniform(0, 50),  # Daily rainfall
            }
            trends.insert(0, data_point)  # Insert at beginning for chronological order
            
        return trends
