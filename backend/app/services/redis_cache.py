import redis
import json
from pathlib import Path
from typing import Optional

METADATA_FILE = Path("metadata_api.json")
REDIS_HOST = "localhost"
REDIS_PORT = 6379
TTL_SECONDS = 3600

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def load_metadata_to_cache():
    if not METADATA_FILE.exists():
        raise FileNotFoundError("metadata_api.json not found")
    with open(METADATA_FILE, "r") as f:
        metadata = json.load(f)
        for vehicle_id, details in metadata.items():
            redis_client.setex(vehicle_id, TTL_SECONDS, json.dumps(details))

def get_metadata(vehicle_id: str) -> Optional[dict]:
    try:
        cached = redis_client.get(vehicle_id)
        if cached:
            return json.loads(cached)
        return None
    except redis.RedisError:
        return None

def is_valid_speed(vehicle_id: str, speed_kmh: float) -> bool:
    metadata = get_metadata(vehicle_id)
    if not metadata:
        return False
    max_speed = metadata.get("max_speed", 100)
    return speed_kmh <= max_speed
