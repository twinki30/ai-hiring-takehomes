import unittest
from unittest.mock import patch, MagicMock
from app.services import dynamodb_batch_writer

class TestDynamoDBWriter(unittest.TestCase):
    @patch("app.services.dynamodb_batch_writer.table")
    @patch("app.services.dynamodb_batch_writer.calculate_distance_from_depot")
    def test_batch_write_to_dynamodb(self, mock_distance, mock_table):
        mock_distance.return_value = 5.0
        mock_batch_writer = MagicMock()
        mock_table.batch_writer.return_value.__enter__.return_value = mock_batch_writer

        sample_data = [{
            'vehicle_id': 'VH_12345',
            'timestamp': '2023-01-01T00:00:00Z',
            'lat': 40.7128,
            'lon': -74.0060,
            'speed_kmh': 50,
            'engine_status': 'moving',
            'fuel_level': 80
        }]

        dynamodb_batch_writer.batch_write_to_dynamodb(sample_data)
        mock_batch_writer.put_item.assert_called_once()
