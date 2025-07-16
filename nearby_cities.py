# nearby_cities.py

import pandas as pd
from math import radians, cos, sin, asin, sqrt

# Load dataset once
cities_df = pd.read_csv("worldcities.csv")
indian_cities = cities_df[cities_df["country"] == "India"]

# Haversine distance formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    return R * 2 * asin(sqrt(a))

# Get nearby cities within a given radius (e.g. 50 km)
def get_nearby_cities(lat, lon, radius_km=50):
    nearby = []

    for _, row in indian_cities.iterrows():
        dist = haversine(lat, lon, row["lat"], row["lng"])
        if dist <= radius_km:
            nearby.append({
                "city": row["city"],
                "lat": row["lat"],
                "lon": row["lng"],
                "distance_km": round(dist, 1)
            })
    
    return sorted(nearby, key=lambda x: x["distance_km"])
