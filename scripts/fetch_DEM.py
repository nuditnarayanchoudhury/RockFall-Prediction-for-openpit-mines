# --------------------------------------------------------
# DEM Feature Extraction Script (GDAL-Free Version)
# --------------------------------------------------------

import rasterio
import numpy as np
import pandas as pd
import os

# --------------------------------------------------------
# 1. Input DEM (.dt2) file path (YOUR uploaded file)
# --------------------------------------------------------
dt2_path = "../dataset/n07_e080_1arc_v3.dt2"   # your DEM file
output_csv = "dem_features.csv"

# --------------------------------------------------------
# 2. Load DEM (.dt2) DIRECTLY with Rasterio
# --------------------------------------------------------
if not os.path.exists(dt2_path):
    raise FileNotFoundError(f"DEM file not found: {dt2_path}")

with rasterio.open(dt2_path) as src:
    dem_full = src.read(1)
    transform = src.transform
    nodata = src.nodata

# --------------------------------------------------------
# 3. Mask NoData
# --------------------------------------------------------
if nodata is not None:
    dem_full = np.where(dem_full == nodata, np.nan, dem_full)

# --------------------------------------------------------
# 4. Downsample DEM to reduce memory usage
# --------------------------------------------------------
sample_rate = 10  # adjust based on DEM size

dem = dem_full[::sample_rate, ::sample_rate]
rows, cols = dem.shape

print("DEM Loaded:")
print("Original shape:", dem_full.shape)
print("Sampled shape:", dem.shape)
print("Elevation min/max:", np.nanmin(dem), np.nanmax(dem))

# --------------------------------------------------------
# 5. Compute Slope and Aspect
# --------------------------------------------------------
y, x = np.gradient(dem, edge_order=2)

slope = np.arctan(np.sqrt(x**2 + y**2)) * (180 / np.pi)

aspect = np.arctan2(-x, y) * (180 / np.pi)
aspect = np.where(aspect < 0, 360 + aspect, aspect)

# --------------------------------------------------------
# 6. Compute Latitude & Longitude for each pixel
# --------------------------------------------------------
lats = np.zeros((rows, cols))
lons = np.zeros((rows, cols))

for i in range(rows):
    for j in range(cols):
        lon, lat = rasterio.transform.xy(transform, i * sample_rate, j * sample_rate)
        lats[i, j] = lat
        lons[i, j] = lon

# --------------------------------------------------------
# 7. Create DataFrame
# --------------------------------------------------------
dem_df = pd.DataFrame({
    "latitude": lats.ravel(),
    "longitude": lons.ravel(),
    "elevation": dem.ravel(),
    "slope": slope.ravel(),
    "aspect": aspect.ravel()
})

# --------------------------------------------------------
# 8. Save CSV
# --------------------------------------------------------
dem_df.to_csv(output_csv, index=False)
print("DEM features saved to:", output_csv)
