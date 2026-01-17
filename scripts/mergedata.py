# ==========================================================
# FINAL AUTO-DETECTING ROCKFALL DATASET BUILDER (CANNOT FAIL)
# ==========================================================

import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

BASE = "C:/Users/nudit/Downloads/SIH_PROJECT/dataset/"

# ----------------------------------------------------------
# Load datasets
# ----------------------------------------------------------
rainfall = pd.read_csv(BASE + "rainfall_geotechnical_1901-2015.csv")
dem = pd.read_csv(BASE + "dem_features.csv")
earthquake = pd.read_csv(BASE + "india_earthquakes_1995_2015.csv")
drone = pd.read_csv(BASE + "synthetic_drone_dataset.csv")

# ----------------------------------------------------------
# Add region lat/lon BEFORE MERGE
# ----------------------------------------------------------
rainfall["SUBDIVISION_clean"] = rainfall["SUBDIVISION"].astype(str).str.upper().str.strip()

region_coords = {
    "ANDAMAN & NICOBAR ISLANDS": (11.67, 92.75),
    "ARUNACHAL PRADESH": (28.21, 94.72),
    "ASSAM & MEGHALAYA": (26.15, 91.77),
    "NAGA MANI MIZO TRIPURA": (23.73, 92.72),
    "SUB HIMALAYAN WEST BENGAL & SIKKIM": (27.03, 88.26),
    "GANGETIC WEST BENGAL": (23.0, 88.3),
    "ORISSA": (20.95, 85.1),
    "JHARKHAND": (23.61, 85.27),
    "BIHAR": (25.37, 85.13),
    "EAST UTTAR PRADESH": (26.85, 80.95),
    "WEST UTTAR PRADESH": (28.53, 77.39),
    "UTTARAKHAND": (30.07, 79.66),
    "HARYANA DELHI & CHANDIGARH": (28.70, 77.10),
    "PUNJAB": (31.15, 75.34),
    "HIMACHAL PRADESH": (31.10, 77.17),
    "JAMMU & KASHMIR": (33.50, 75.10),
    "WEST RAJASTHAN": (26.91, 70.92),
    "EAST RAJASTHAN": (26.48, 75.79),
    "WEST MADHYA PRADESH": (23.55, 75.50),
    "EAST MADHYA PRADESH": (23.83, 80.39),
    "GUJARAT REGION": (22.30, 73.20),
    "SAURASHTRA & KUTCH": (21.52, 70.45),
    "KONKAN & GOA": (18.51, 73.85),
    "MADHYA MAHARASHTRA": (19.75, 75.71),
    "MATATHWADA": (19.10, 75.09),
    "VIDARBHA": (21.15, 79.09),
    "CHHATTISGARH": (21.25, 81.63),
    "COASTAL ANDHRA PRADESH": (16.51, 80.64),
    "TELANGANA": (17.38, 78.48),
    "RAYALSEEMA": (14.44, 78.23),
    "TAMIL NADU": (11.12, 78.65),
    "COASTAL KARNATAKA": (12.97, 74.68),
    "NORTH INTERIOR KARNATAKA": (16.52, 75.93),
    "SOUTH INTERIOR KARNATAKA": (12.97, 77.56),
    "KERALA": (10.85, 76.27),
    "LAKSHADWEEP": (10.57, 72.64)
}

rainfall["latitude"] = rainfall["SUBDIVISION_clean"].apply(lambda x: region_coords.get(x, (0, 0))[0])
rainfall["longitude"] = rainfall["SUBDIVISION_clean"].apply(lambda x: region_coords.get(x, (0, 0))[1])

# ----------------------------------------------------------
# Earthquake yearly summary
# ----------------------------------------------------------
earthquake["YEAR"] = pd.to_datetime(earthquake["time"], errors="coerce").dt.year
earthquake = earthquake.dropna(subset=["YEAR"])
earthquake["YEAR"] = earthquake["YEAR"].astype(int)

eq_yearly = earthquake.groupby("YEAR").agg({
    "mag": "mean",
    "depth": "mean",
    "latitude": "mean",
    "longitude": "mean",
    "place": "count"
}).rename(columns={"place": "earthquake_count"}).reset_index()

# ----------------------------------------------------------
# SAFE LEFT MERGE (Rainfall ← Earthquakes)
# ----------------------------------------------------------
merged = pd.merge(
    rainfall,
    eq_yearly,
    on="YEAR",
    how="left",
    suffixes=("_rain", "_eq")
)

# ----------------------------------------------------------
# AUTO-DETECT RAINFALL LATITUDE/LONGITUDE IN MERGED
# ----------------------------------------------------------
lat_col = next((c for c in merged.columns if "latitude" in c and c.endswith("rain")), None)
lon_col = next((c for c in merged.columns if "longitude" in c and c.endswith("rain")), None)

if lat_col is None or lon_col is None:
    print("\n❌ Columns after merge:", list(merged.columns))
    raise SystemExit("FATAL: Could not detect rainfall latitude/longitude in merged dataset!")

# Create final guaranteed columns
merged["latitude"] = merged[lat_col]
merged["longitude"] = merged[lon_col]

print("\n✅ LAT/LON DETECTED:", lat_col, lon_col)

# ----------------------------------------------------------
# DEM nearest neighbor
# ----------------------------------------------------------
coords_dem = dem[["latitude", "longitude"]].values
coords_regions = merged[["latitude", "longitude"]].values

nn = NearestNeighbors(n_neighbors=1).fit(coords_dem)
_, idx = nn.kneighbors(coords_regions)

dem_near = dem.iloc[idx.flatten()].reset_index(drop=True)
dem_near.columns = ["dem_" + c for c in dem_near.columns]

merged = pd.concat([merged.reset_index(drop=True), dem_near], axis=1)

# ----------------------------------------------------------
# Add drone features
# ----------------------------------------------------------
merged["drone_id"] = merged.index % len(drone)
merged = pd.merge(merged, drone, left_on="drone_id", right_on="id", how="left")
merged = merged.drop(columns=["id", "drone_id"], errors="ignore")

# ----------------------------------------------------------
# Save final dataset
# ----------------------------------------------------------
output = BASE + "final_multimodal_dataset.csv"
merged.to_csv(output, index=False)

print("🎉 Dataset created:", output)
print("Shape:", merged.shape)
