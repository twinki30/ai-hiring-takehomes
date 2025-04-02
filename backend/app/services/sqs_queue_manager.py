import boto3

sqs = boto3.client('sqs')

def publish_to_sqs(data):
    queue_url = 'your-sqs-queue-url'
    message = {
        'vehicle_id': data['vehicle_id'],
        'timestamp': data['timestamp'],
        'lat': data['lat'],
        'lon': data['lon'],
        'speed_kmh': data['speed_kmh'],
        'engine_status': data['engine_status'],
        'fuel_level': data['fuel_level']
    }

    # Set priority based on engine status
    priority = 1 if data['engine_status'] == 'moving' else 10

    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message),
        MessageAttributes={
            'Priority': {
                'DataType': 'Number',
                'StringValue': str(priority)
            }
        }
    )
