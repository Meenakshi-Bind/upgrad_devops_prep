from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

AWS_API_URL = "https://ko01rlagql.execute-api.us-east-1.amazonaws.com/chairdata"


data_store = []

def process_data(data):
    alerts = []

    if data.get("posture_angle", 0) > 40:
        alerts.append("Bad posture")

    if not data.get("movement", True):
        alerts.append("User inactive")

    data["alerts"] = alerts
    return data

@app.route("/sensor-data", methods=["POST"])
def receive_data():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    processed = process_data(data)
    data_store.append(processed)

    try:
        response = requests.post(AWS_API_URL, json=processed, timeout=5)
        print("Cloud response:", response.status_code, response.text)
    except Exception as e:
        print("Error sending to cloud:", e)

    return jsonify({"status": "sent to cloud"})

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/data")
def api_data():
    return jsonify(data_store)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)