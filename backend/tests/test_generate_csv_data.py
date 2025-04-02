import unittest
from unittest.mock import patch, mock_open
from io import StringIO
from decimal import Decimal
from app.scripts.generate_csv_data import batch_write_to_dynamodb, calculate_distance_from_depot

class TestGenerateCSVData(unittest.TestCase):

    @patch('app.scripts.generate_csv_data.get_metadata')
    def test_calculate_distance_from_depot(self, mock_get_metadata):
        mock_get_metadata.return_value = {
            'depot_lat': 40.7128,
            'depot_lon': -74.0060
        }
        record = {
            'vehicle_id': 'VH_00001',
            'lat': 40.730610,
            'lon': -73.935242
        }
        distance = calculate_distance_from_depot(record)
        self.assertTrue(isinstance(distance, float))
        self.assertGreater(distance, 0)

    @patch('app.scripts.generate_csv_data.table')
    @patch('app.scripts.generate_csv_data.calculate_distance_from_depot')
    def test_batch_write_to_dynamodb(self, mock_distance, mock_table):
        mock_distance.return_value = 5.5
        mock_batch_writer = mock_table.batch_writer.return_value.__enter__.return_value

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

        mock_batch_writer.put_item.assert_called_once()
        called_item = mock_batch_writer.put_item.call_args[1]['Item']
        self.assertEqual(called_item['vehicle_id'], 'VH_00001')
        self.assertEqual(called_item['distance_from_depot'], Decimal('5.5'))

if __name__ == '__main__':
    unittest.main()
