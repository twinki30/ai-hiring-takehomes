import boto3
import json
import os
from typing import Dict

# These are dummy queue URLs for local/mocked testing
def get_mock_queues():
    return {
        "moving": "http://localhost:4566/000000000000/moving-queue",
        "idle": "http://localhost:4566/000000000000/idle-queue"
    }

sqs = boto3.client("sqs", region_name="us-east-1", endpoint_url="http://localhost:4566")

queues = get_mock_queues()


def publish_to_sqs(record: Dict):
    try:
        engine_status = record.get("engine_status", "idle")
        queue_url = queues["moving"] if engine_status == "moving" else queues["idle"]

        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(record)
        )
        print(f"Published to {engine_status} queue: {response['MessageId']}")
    except Exception as e:
        print(f"Error publishing to SQS: {e}")

# Example usage
if __name__ == "__main__":
    test_event = {
        "vehicle_id": "VH_00001",
        "timestamp": "2023-10-10T12:00:00",
        "lat": 40.7128,
        "lon": -74.0060,
        "speed_kmh": 45,
        "engine_status": "moving",
        "fuel_level": 75
    }
    publish_to_sqs(test_event)
