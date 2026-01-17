import requests
import os

url = (
    "https://earthquake.usgs.gov/fdsnws/event/1/query?"
    "format=csv"
    "&starttime=1995-01-01"
    "&endtime=2015-12-31"
    "&minmagnitude=2.5"
    "&latitude=22.0"
    "&longitude=79.0"
    "&maxradiuskm=2000"
)


response = requests.get(url)
if response.status_code == 200:
    with open("../dataset/india_earthquakes_1995_2015.csv", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("✅ Seismic data saved to india_earthquakes_1995_2015.csv")
else:
    print("❌ Failed to fetch data:", response.status_code)
