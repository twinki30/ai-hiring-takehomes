import json
import redis
from datetime import timedelta

# Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def load_metadata(metadata_file_path="metadata_api.json"):
   """ Load the metadata file and return as a dictionary. """
   try:
       with open(metadata_file_path, "r") as file:
           metadata = json.load(file)
       return metadata
   except FileNotFoundError:
       print(f"Metadata file {metadata_file_path} not found.")
       return {}

def cache_metadata(metadata):
   """ Cache metadata in Redis with a TTL of 1 hour. """
   redis_client.setex("vehicle_metadata", timedelta(hours=1), json.dumps(metadata))

def get_cached_metadata():
   """ Retrieve metadata from Redis cache. """
   cached_data = redis_client.get("vehicle_metadata")
   if cached_data:
       return json.loads(cached_data)
   else:
       # Cache miss, load and cache fresh data
       metadata = load_metadata()
       cache_metadata(metadata)
       return metadata

if __name__ == "__main__":
   metadata = get_cached_metadata()
   print("Metadata loaded and cached.")
