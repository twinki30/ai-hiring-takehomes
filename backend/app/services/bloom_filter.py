from pybloom_live import BloomFilter

bloom_filter = BloomFilter(capacity=1000000, error_rate=0.001)

def check_and_add_to_bloom_filter(vehicle_id, timestamp):
    key = f"{vehicle_id}_{timestamp}"
    if key in bloom_filter:
        return False  # Duplicate found
    bloom_filter.add(key)
    return True
