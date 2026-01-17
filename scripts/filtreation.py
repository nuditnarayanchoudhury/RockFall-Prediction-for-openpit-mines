import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# -----------------------------
# 1. Load Dataset
# -----------------------------
file_path = "../dataset/refined_sih_dataset.csv"  # adjust path if needed
df = pd.read_csv(file_path)

# -----------------------------
# 2. Drop redundant/metadata columns
# -----------------------------
drop_cols = [
    "id_x", "id_y", "net", "status", "updated", "place", "magSource", "magType",
    "locationSource", "type"
]

# Drop duplicate lat/long (keep only latitude_x, longitude_x)
if "latitude_y" in df.columns:
    drop_cols.append("latitude_y")
if "longitude_y" in df.columns:
    drop_cols.append("longitude_y")

df_clean = df.drop(columns=[c for c in drop_cols if c in df.columns])

# -----------------------------
# 3. Process time column
# -----------------------------
if "time" in df_clean.columns:
    df_clean["time"] = pd.to_datetime(df_clean["time"], errors="coerce")
    df_clean["year"] = df_clean["time"].dt.year
    df_clean["month"] = df_clean["time"].dt.month
    df_clean["day"] = df_clean["time"].dt.day
    df_clean["season"] = df_clean["month"] % 12 // 3 + 1  # 1=winter,2=spring,3=summer,4=fall
    df_clean = df_clean.drop(columns=["time"])

# -----------------------------
# 4. Define Target Label
# -----------------------------
if "crack_density" in df_clean.columns and "SeismicVibration_mm/s" in df_clean.columns:
    df_clean["rockfall_risk"] = (
        (df_clean["crack_density"] > df_clean["crack_density"].median()) |
        (df_clean["SeismicVibration_mm/s"] > df_clean["SeismicVibration_mm/s"].median())
    ).astype(int)

# -----------------------------
# 5. Normalize numeric features
# -----------------------------
numeric_cols = df_clean.select_dtypes(include=["int64", "float64"]).columns.tolist()
if "rockfall_risk" in numeric_cols:
    numeric_cols.remove("rockfall_risk")

scaler = MinMaxScaler()
df_clean[numeric_cols] = scaler.fit_transform(df_clean[numeric_cols])

# -----------------------------
# 6. Save ML-ready dataset
# -----------------------------
df_clean.to_csv("../dataset/refined_sih_dataset_ML_ready.csv", index=False)

print("✅ ML-ready dataset saved as refined_sih_dataset_ML_ready.csv")
print("Shape:", df_clean.shape)
print("Columns:", df_clean.columns[:20].tolist(), "...")
