import unittest
from unittest.mock import patch, MagicMock
from app.services import sqs_publisher

class TestSQSPublisher(unittest.TestCase):
    @patch("app.services.sqs_publisher.sqs")
    def test_publish_to_sqs_moving(self, mock_sqs):
        mock_sqs.send_message.return_value = {"MessageId": "msg-123"}
        record = {
            "vehicle_id": "VH_001",
            "engine_status": "moving"
        }
        sqs_publisher.publish_to_sqs(record)
        mock_sqs.send_message.assert_called_once()

    @patch("app.services.sqs_publisher.sqs")
    def test_publish_to_sqs_idle(self, mock_sqs):
        mock_sqs.send_message.return_value = {"MessageId": "msg-456"}
        record = {
            "vehicle_id": "VH_002",
            "engine_status": "idle"
        }
        sqs_publisher.publish_to_sqs(record)
        mock_sqs.send_message.assert_called_once()
