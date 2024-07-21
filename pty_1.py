# import math

# def haversine(lat1, lon1, lat2, lon2):
#     R = 6371.0  # Earth radius in kilometers
    
#     # Convert latitude and longitude from degrees to radians
#     lat1_rad = math.radians(lat1)
#     lon1_rad = math.radians(lon1)
#     lat2_rad = math.radians(lat2)
#     lon2_rad = math.radians(lon2)

#     print(f"lat1_rad: {lat1_rad}, lon1_rad: {lon1_rad}")
#     print(f"lat2_rad: {lat2_rad}, lon2_rad: {lon2_rad}")

#     # Differences in coordinates
#     dlat = lat2_rad - lat1_rad
#     dlon = lon2_rad - lon1_rad

#     print(f"dlat: {dlat}, dlon: {dlon}")

#     # Haversine formula
#     a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

#     print(f"a: {a}, c: {c}")

#     distance = R * c
#     return distance

# # Test the function with your coordinates
# lat1 = 31.470197677612305
# lon1 = 74.47039031982422
# lat2 = 31.4638336
# lon2 = 74.4456192

# distance = haversine(lat1, lon1, lat2, lon2)
# print(f"Calculated distance: {distance} km")


import math
from geopy.distance import geodesic

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers
    
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

# Coordinates for New York City and Los Angeles
lat1, lon1 = 40.7128, -74.0060
lat2, lon2 = 34.0522, -118.2437

# Calculate distance using Haversine function
distance_haversine = haversine(lat1, lon1, lat2, lon2)
print(f"Calculated distance using Haversine: {distance_haversine} km")

# Calculate distance using geopy
distance_geopy = geodesic((lat1, lon1), (lat2, lon2)).km
print(f"Calculated distance using geopy: {distance_geopy} km")


