import requests
import json

# Test data (from your original file)
test_data = {
    "body": json.dumps({
        "features": {
            "yr": 1,
            "mnth": 7,
            "hr": 17,
            "holiday": 0,
            "weekday": 4,
            "workingday": 1,
            "temp": 0.65,
            "atemp": 0.7,
            "hum": 0.5,
            "windspeed": 0.1,
            "season_2": 0,
            "season_3": 1,
            "season_4": 0,
            "weathersit_2": 0,
            "weathersit_3": 1,
            "weathersit_4": 0
        }
    })
}

try:
    response = requests.post(
        "http://localhost:9000/2015-03-31/functions/function/invocations",
        json=test_data,
        timeout=30
    )
    
    print("Status Code:", response.status_code)
    print("Response:", response.json())
    
except Exception as e:
    print("Error:", e) 