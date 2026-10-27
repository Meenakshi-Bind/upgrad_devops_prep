Project Description

The Smart Chair Health Monitoring System is an IoT-based application designed to monitor the posture and activity of office workers. The system simulates multiple health related sensors such as seat pressure, posture angle, heart rate, temperature, and movement detection.

Sensor data is generated using a Python simulator and sent to a fog node running on an AWS EC2 instance. The fog node processes the data, detects alerts such as bad posture or in activity, and forwards the processed data to the AWS cloud backend.

The cloud backend uses API Gateway, Lambda, SQS, and DynamoDB to process, store, and manage the sensor data. A web dashboard built with HTML and Chart.js visualizes the live sensor readings and alerts in real time.

This architecture demonstrates a scalable fog-to-cloud IoT system using AWS services.

Sensors Used

The system simulates the following sensors:

Seat Pressure Sensor
Posture Angle Sensor
Heart Rate Sensor
Temperature Sensor
Movement Detection Sensor

Sensor Simulator -- > Fog Node (EC2 + Flask) --> API Gateway --> Lambda (Ingestion) --> SQS Queue --> Lambda (Processor) --> DynamoDB --> Web Dashboard (Chart.js)

Flow of Resources

Sensor Simulator - Generates mock sensor data using Python.
Fog Node (EC2) - Receives sensor data.
Processes the data and detects alerts.
API Gateway - Provides a public API endpoint for sending sensor data to AWS.
Lambda (Ingestion) - Receives data from API Gateway.
Sends the data to an SQS queue.
SQS Queue - Buffers incoming messages and enables scalable processing.
Lambda (Processor) - Reads messages from SQS.
Stores the processed data in DynamoDB.
DynamoDB - Stores time-series sensor readings.
Dashboard - Displays sensor readings, graphs, and alerts in real time.