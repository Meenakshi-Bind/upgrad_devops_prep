from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AWS_API_URL = "PASTE_YOUR_API_GATEWAY_URL_HERE"

def process_data(data):
    alerts = []

    if data["posture_angle"] > 40:
        alerts.append("Bad posture")

    if not data["movement"]:
        alerts.append("User inactive")

    data["alerts"] = alerts
    return data

@app.route("/sensor-data", methods=["POST"])
def receive_data():
    data = request.json
    processed_data = process_data(data)

    print("Processed:", processed_data)

    # Send to AWS
    requests.post(AWS_API_URL, json=processed_data)

    return jsonify({"status": "sent to cloud"})

if __name__ == "__main__":
    app.run(port=5000)
    