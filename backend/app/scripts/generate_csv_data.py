import boto3
import json
from app.services.redis_cache import get_metadata
from decimal import Decimal

# DynamoDB table name and client initialization
DYNAMODB_TABLE_NAME = "TelemetryData"

# DynamoDB client setup for LocalStack
dynamodb = boto3.resource(
   'dynamodb',
   region_name='us-east-1',
   endpoint_url='http://localhost:4566',  # LocalStack endpoint
   aws_access_key_id='test',
   aws_secret_access_key='test'
)
table = dynamodb.Table(DYNAMODB_TABLE_NAME)

# Batch write function
def batch_write_to_dynamodb(records: list):
   with table.batch_writer() as batch:
       for record in records:
           try:
               item = {
                   'vehicle_id': record['vehicle_id'],
                   'timestamp': record['timestamp'],
                   'lat': Decimal(str(record['lat'])),  # Convert float to Decimal
                   'lon': Decimal(str(record['lon'])),  # Convert float to Decimal
                   'speed_kmh': Decimal(str(record['speed_kmh'])),  # Convert float to Decimal
                   'engine_status': record['engine_status'],
                   'fuel_level': Decimal(str(record['fuel_level'])),  # Convert float to Decimal
                   'distance_from_depot': Decimal(str(calculate_distance_from_depot(record)))  # Convert float to Decimal
               }
               batch.put_item(Item=item)
           except Exception as e:
               print(f"Error writing record to DynamoDB: {e}")

# Helper function to calculate distance from depot (Haversine formula)
def calculate_distance_from_depot(record: dict) -> float:
   try:
       depot_lat = get_metadata(record['vehicle_id'])['depot_lat']
       depot_lon = get_metadata(record['vehicle_id'])['depot_lon']
   except KeyError:
       print(f"Metadata for vehicle {record['vehicle_id']} not found.")
       return 0  # Return 0 if metadata is not found
   lat1, lon1 = record['lat'], record['lon']
   lat2, lon2 = depot_lat, depot_lon
   import math
   R = 6371  # Earth radius in kilometers
   dlat = math.radians(lat2 - lat1)
   dlon = math.radians(lon2 - lon1)
   a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
   c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
   distance = R * c  # Distance in kilometers
   return distance

if __name__ == "__main__":
   test_records = [
       {
           'vehicle_id': 'VH_00001',
           'timestamp': '2023-10-10T12:00:00',
           'lat': 40.7128,
           'lon': -74.0060,
           'speed_kmh': 45,
           'engine_status': 'moving',
           'fuel_level': 75
       }
   ]
   batch_write_to_dynamodb(test_records)
