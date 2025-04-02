import unittest
from unittest.mock import patch, MagicMock
from app.services import redis_cache

class TestRedisCache(unittest.TestCase):
    @patch("app.services.redis_cache.redis_client")
    def test_get_metadata_hit(self, mock_redis):
        mock_redis.get.return_value = '{"max_speed": 100, "depot_lat": 40.7128, "depot_lon": -74.0060}'
        result = redis_cache.get_metadata("VH_001")
        self.assertEqual(result["max_speed"], 100)

    @patch("app.services.redis_cache.redis_client")
    def test_is_valid_speed_true(self, mock_redis):
        mock_redis.get.return_value = '{"max_speed": 100}'
        result = redis_cache.is_valid_speed("VH_001", 80)
        self.assertTrue(result)

    @patch("app.services.redis_cache.redis_client")
    def test_is_valid_speed_false(self, mock_redis):
        mock_redis.get.return_value = '{"max_speed": 60}'
        result = redis_cache.is_valid_speed("VH_001", 80)
        self.assertFalse(result)
