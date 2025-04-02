import unittest
from unittest.mock import patch, MagicMock
from app.scripts.lambda_handler import lambda_handler

class TestLambdaHandler(unittest.TestCase):

    @patch('app.scripts.lambda_handler.batch_write_to_dynamodb')
    @patch('app.scripts.lambda_handler.publish_to_sqs')
    @patch('app.scripts.lambda_handler.get_metadata')
    def test_lambda_handler_valid_data(self, mock_get_metadata, mock_publish_to_sqs, mock_batch_write_to_dynamodb):
        # Mock metadata and valid record
        mock_get_metadata.return_value = {'depot_lat': 40.7128, 'depot_lon': -74.0060, 'max_speed': 120}

        event = {
            'Records': [
                {
                    'body': '{"vehicle_id": "VH_001", "lat": 40.7128, "lon": -74.0060, "speed_kmh": 100, "engine_status": "moving"}'
                }
            ]
        }

        context = {}

        lambda_handler(event, context)

        # Check if batch write to DynamoDB was called
        mock_batch_write_to_dynamodb.assert_called_once()

        # Check if publish to SQS was called
        mock_publish_to_sqs.assert_called_once()

    @patch('app.scripts.lambda_handler.get_metadata')
    def test_lambda_handler_invalid_speed(self, mock_get_metadata):
        # Mock metadata for invalid speed
        mock_get_metadata.return_value = {'depot_lat': 40.7128, 'depot_lon': -74.0060, 'max_speed': 100}

        event = {
            'Records': [
                {
                    'body': '{"vehicle_id": "VH_001", "lat": 40.7128, "lon": -74.0060, "speed_kmh": 150, "engine_status": "moving"}'
                }
            ]
        }

        context = {}

        lambda_handler(event, context)

        # Check that batch write to DynamoDB was NOT called
        mock_batch_write_to_dynamodb.assert_not_called()
        # Check that publish to SQS was NOT called
        mock_publish_to_sqs.assert_not_called()

if __name__ == "__main__":
    unittest.main()
