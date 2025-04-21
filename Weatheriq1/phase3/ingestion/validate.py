def is_valid_weather(data):
    required_fields = ["temperature", "humidity", "pressure"]
    for field in required_fields:
        if data.get(field) is None:
            return False
    return True
