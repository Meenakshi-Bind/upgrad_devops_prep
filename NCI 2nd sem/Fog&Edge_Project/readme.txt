Smart Chair Health Monitoring System
Installation and Deployment Steps

--------------------------------------------------
1. Infrastructure Setup Using Terraform
--------------------------------------------------

First, the AWS infrastructure for the project was created using Terraform.

Resources created:

- EC2 Instance (Fog Node)
- DynamoDB Table (SmartChairData)
- SQS Queue (smartchair-queue)
- Lambda Functions (Ingestion and Processor)
- API Gateway Endpoint
- IAM Roles and Permissions

Commands used:

terraform init
terraform plan
terraform apply

After running these commands, all required AWS resources were created successfully.

--------------------------------------------------
2. Configure EC2 Fog Node
--------------------------------------------------

After the EC2 instance was created, the project files were uploaded to the EC2 server.

Files uploaded:

fog.py
sensor_simulator.py
templates/dashboard.html

Configuration changes:

1. Update API Gateway URL inside fog.py

AWS_API_URL = "YOUR_API_GATEWAY_URL"

2. Update EC2 Public IP inside sensor.py

FOG_URL = "http://EC2_PUBLIC_IP:5000/sensor-data"

--------------------------------------------------
3. Lambda Configuration
--------------------------------------------------

Two Lambda functions are used in the system.

1. Ingestion Lambda
Purpose:
Receives data from API Gateway and sends it to the SQS queue.

Manual configuration:

Add the SQS queue URL inside the Lambda code:

QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/ACCOUNT_ID/smartchair-queue"

2. Processor Lambda
Purpose:
Reads messages from SQS and stores them into DynamoDB.

This Lambda is triggered automatically when new messages arrive in the SQS queue.

--------------------------------------------------
4. Running the Fog Application
--------------------------------------------------

After uploading the files to EC2, the fog node application was started.

Command used:

python3 fog.py

This starts the Flask server that receives sensor data and forwards it to the AWS backend.

--------------------------------------------------
5. Running the Sensor Simulator
--------------------------------------------------

After starting the fog application, the sensor simulator was executed.

Command used:

python3 sensor_simulator.py

The sensor simulator generates mock health monitoring data and sends it to the fog node every few seconds.

--------------------------------------------------
6. Data Processing Flow
--------------------------------------------------

1. Sensor simulator generates chair health data.
2. Data is sent to the fog node using HTTP requests.
3. Fog node processes the data and generates alerts.
4. Processed data is sent to API Gateway.
5. Ingestion Lambda receives the event and sends it to SQS.
6. Processor Lambda reads from SQS and stores the data in DynamoDB.
7. The dashboard retrieves the data and displays it using graphs.

--------------------------------------------------
7. Dashboard Access
--------------------------------------------------

The dashboard can be accessed using the EC2 public IP address:

http://EC2_PUBLIC_IP:5000

The dashboard displays:

- Sensor readings
- Health alerts
- Graphs of posture, heart rate, and temperature
- Real-time monitoring data