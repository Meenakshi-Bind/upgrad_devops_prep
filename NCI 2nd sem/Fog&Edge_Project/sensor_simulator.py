import random
import time
import requests
from datetime import datetime

FOG_URL = "http://44.220.184.42:5000/sensor-data"

while True:
    data = {
        "chair_id": "chair-01",
        "timestamp": datetime.utcnow().isoformat(),
        "seat_pressure": random.randint(60, 100),
        "posture_angle": random.randint(10, 60),
        "heart_rate": random.randint(70, 110),
        "temperature": random.randint(25, 35),
        "movement": random.choice([True, False])
    }

    print(data)

    try:
        response = requests.post(FOG_URL, json=data, timeout=5)
        print("Fog response:", response.status_code, response.text)
    except Exception as e:
        print("Error sending to fog:", e)

    time.sleep(5)