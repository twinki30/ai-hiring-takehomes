def transform_telemetry_data(row):
    vehicle_id = row["vehicle_id"]
    lat, lon = row["lat"], row["lon"]
    metadata = get_metadata(vehicle_id)
    distance_from_depot = calculate_distance(lat, lon, metadata['depot_lat'], metadata['depot_lon'])
    row["distance_from_depot"] = distance_from_depot
    return row
