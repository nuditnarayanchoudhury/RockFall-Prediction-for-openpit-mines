import pandas as pd
import numpy as np

# Load rainfall dataset
df = pd.read_csv("../dataset/rainfall_area-wt_sd_1901-2015.csv")

# Check available columns
print("Columns in dataset:", df.columns)

# Assuming dataset has 'YEAR' and 'ANNUAL' (annual rainfall in mm)
if "ANNUAL" not in df.columns:
    raise ValueError("Dataset must contain 'ANNUAL' rainfall column.")

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic geotechnical features
# Displacement increases with rainfall but with noise
df["Displacement_mm"] = (df["ANNUAL"] * 0.01) + np.random.normal(0, 2, len(df))

# Strain correlates with displacement
df["Strain_micro"] = (df["Displacement_mm"] * 10) + np.random.normal(0, 5, len(df))

# Pore pressure increases with rainfall but capped
df["PorePressure_kPa"] = np.clip((df["ANNUAL"] * 0.05) + np.random.normal(0, 10, len(df)), 0, None)

# Seismic vibration mostly small but with rare spikes
df["SeismicVibration_mm/s"] = np.random.normal(2, 0.5, len(df))
spike_indices = np.random.choice(len(df), size=int(0.05 * len(df)), replace=False)
df.loc[spike_indices, "SeismicVibration_mm/s"] += np.random.uniform(5, 15, len(spike_indices))

# Save enhanced dataset
df.to_csv("../dataset/rainfall_geotechnical_1901-2015.csv", index=False)

print("✅ Geotechnical data added and saved as 'rainfall_geotechnical_1901-2015.csv'")
