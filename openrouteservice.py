import requests

def get_distance_duration(api_key, start_coords, end_coords):
    url = 'https://api.openrouteservice.org/v2/directions/driving-car'
    headers = {'Authorization': api_key}
    params = {
        'start': ','.join(map(str, start_coords)),
        'end': ','.join(map(str, end_coords)),
        'format': 'geojson'
    }
    response = requests.get(url, headers=headers, params=params)
    
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
    
    if response.status_code == 200:
        data = response.json()
        if 'routes' in data and len(data['routes']) > 0:
            distance = data['routes'][0]['summary']['distance'] / 1000  # Convert to kilometers
            duration = data['routes'][0]['summary']['duration'] / 60  # Convert to minutes
            return distance, duration
        else:
            raise Exception("No routes found in the response")
    else:
        raise Exception(f"Error: {response.status_code} {response.text}")

# Example coordinates (longitude, latitude)
start_coords = (-74.0060, 40.7128)  # New York City
end_coords = (-118.2437, 34.0522)  # Los Angeles
api_key = '5b3ce3597851110001cf6248a9bb945f514b4c59a77d29be28989af1'

distance, duration = get_distance_duration(api_key, start_coords, end_coords)
print(f"Distance: {distance:.2f} km, Duration: {duration:.2f} minutes")
