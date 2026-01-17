import pandas as pd
rainfall = pd.read_csv("../dataset/rainfall_geotechnical_1901-2015.csv")
print(rainfall.columns)
print(rainfall["SUBDIVISION"].unique())