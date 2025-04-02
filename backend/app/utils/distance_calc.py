import math
from geopy.distance import geodesic

def calculate_distance(lat1, lon1, lat2, lon2):
   """ Calculate the distance in kilometers between two GPS coordinates. """
   coords_1 = (lat1, lon1)
   coords_2 = (lat2, lon2)
   return geodesic(coords_1, coords_2).kilometers

def get_vehicle_depot_distance(vehicle_id, metadata):
   """ Get distance from the vehicle's current location to the depot. """
   if vehicle_id in metadata:
       vehicle_data = metadata[vehicle_id]
       depot_lat = vehicle_data['depot_lat']
       depot_lon = vehicle_data['depot_lon']
       return depot_lat, depot_lon
   else:
       raise ValueError(f"Metadata for vehicle {vehicle_id} not found.")

def process_telemetry_data(vehicle_id, lat, lon, metadata):
   """ Process telemetry data to calculate the distance from depot. """
   depot_lat, depot_lon = get_vehicle_depot_distance(vehicle_id, metadata)
   distance = calculate_distance(lat, lon, depot_lat, depot_lon)
   return distance

if __name__ == "__main__":
   metadata = load_metadata()  # Load metadata from file
   vehicle_id = "VH_001"
   lat, lon = 40.730610, -73.935242  # Sample telemetry coordinates (New York)

   distance = process_telemetry_data(vehicle_id, lat, lon, metadata)
   print(f"Distance from depot: {distance:.2f} km")
