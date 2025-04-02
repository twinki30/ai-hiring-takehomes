import json
from app.services.dynamodb_batch_writer import batch_write_to_dynamodb
from app.services.sqs_publisher import publish_to_sqs
from app.services.redis_cache import get_metadata

def lambda_handler(event, context):
    for record in event['Records']:
        # Parse the message and process the data
        data = json.loads(record['body'])
        vehicle_id = data.get('vehicle_id')
        lat = data.get('lat')
        lon = data.get('lon')
        speed_kmh = data.get('speed_kmh')

        # Validate data
        if is_valid_speed(vehicle_id, speed_kmh):
            # Calculate distance from depot
            metadata = get_metadata(vehicle_id)
            distance = calculate_distance(lat, lon, metadata['depot_lat'], metadata['depot_lon'])

            # Write valid record to DynamoDB
            batch_write_to_dynamodb([data])

            # Optionally publish to SQS if required
            publish_to_sqs(data)
        else:
            print(f"Invalid data for vehicle {vehicle_id}")
