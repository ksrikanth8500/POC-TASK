def transform_realtime(json_data):
    return {
        "timestamp": json_data.get("dt"),
        "temperature": json_data["main"].get("temp"),
        "humidity": json_data["main"].get("humidity"),
        "pressure": json_data["main"].get("pressure"),
        "wind_speed": json_data["wind"].get("speed"),
        "description": json_data["weather"][0].get("description") if json_data.get("weather") else None,
    }
