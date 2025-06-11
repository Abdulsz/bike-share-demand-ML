Bike Share Demand Prediction API
A containerized machine learning API that predicts bike sharing demand using a Random Forest model, deployed on AWS Lambda.

Overview
This project serves real-time predictions of bike share demand based on time, weather, and seasonal features. The model is trained offline, serialized, and deployed in a Docker container to AWS Lambda using the container image feature.

Architecture
JSON input with 16 features

Processed by AWS Lambda container

Model returns predicted bike demand

Response formatted in JSON

Features
Serverless ML inference (AWS Lambda)

Fast response time (~200ms warm start)

Scalable auto-execution

RESTful JSON API

CORS support

Built-in health and error handling

Requirements
Docker

AWS CLI with permissions

Python 3.11+

AWS account (with ECR and Lambda enabled)

Project Structure

bike-share-aws/
├── Dockerfile
├── bike-share.py
├── requirements.txt
├── random_forest_bike_model.pkl
├── test_container.py
├── deploy_to_aws.ps1
├── api_gateway_example.py
└── README.md
Installation & Setup
Clone the repo and navigate into it

Build the container:
docker build -t bike-share-lambda .

(Optional) Run locally:
docker run --rm -p 9000:8080 bike-share-lambda:latest

Deployment Options

Manual
Create an ECR repo and push your container image

Create a Lambda function via the AWS Console using the ECR image

Local & Lambda Testing
Use test_container.py to send test input to a locally running container.
For Lambda, use the AWS CLI to invoke with a JSON payload.

Model Details
Algorithm: Random Forest Regressor

Input Features: 16 weather/time-related variables

Output: Continuous bike demand prediction

Size: ~7.9MB

Trained with scikit-learn 1.6.1

Performance
Container Size: ~1.74GB

Cold Start Time: 2-3 seconds

Warm Response Time: ~200ms

Memory: 512MB

Auto-scaled concurrency

Security
Uses environment variables, not hardcoded secrets

IAM role-based AWS access

Input sanitization and error responses
