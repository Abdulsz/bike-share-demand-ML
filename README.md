# 🚴‍♂️ Bike Share Demand Prediction API

A containerized machine learning API that predicts bike sharing demand using a Random Forest model, deployed as an AWS Lambda function.

## 📊 Overview

This project deploys a pre-trained Random Forest model to predict bike sharing demand based on weather conditions, time of day, and seasonal factors. The model is containerized using Docker and can be deployed to AWS Lambda for serverless inference.

## 🏗️ Architecture

```
Input Features (JSON)
    ↓
AWS Lambda Container
    ↓
Random Forest Model
    ↓
Bike Demand Prediction
    ↓
JSON Response
```

## 🚀 Features

- **Serverless ML Inference**: AWS Lambda container deployment
- **Fast Predictions**: ~200ms response time (warm starts)
- **Scalable**: Auto-scaling with AWS Lambda
- **RESTful API**: JSON input/output format
- **CORS Enabled**: Ready for web applications
- **Health Checks**: Built-in health monitoring
- **Error Handling**: Comprehensive error responses

## 📋 Requirements

- Docker
- AWS CLI configured
- AWS account with ECR and Lambda permissions
- Python 3.11+

## 🛠️ Project Structure

```
bike-share-aws/
├── Dockerfile                    # Container definition
├── bike-share.py                # Lambda handler
├── requirements.txt             # Python dependencies
├── random_forest_bike_model.pkl # Trained ML model
├── test_container.py           # Local testing script
├── deploy_to_aws.ps1           # Deployment automation
├── api_gateway_example.py      # API Gateway integration
└── README.md                   # This file
```

## 🔧 Installation & Setup

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd bike-share-aws
```

### 2. Build Docker Container

```bash
docker build -t bike-share-lambda .
```

### 3. Test Locally (Optional)

```bash
# Start container
docker run --rm -p 9000:8080 bike-share-lambda:latest

# Test in another terminal
python test_container.py
```

## 🚀 Deployment to AWS

### Option 1: Automated Deployment

```bash
# Configure your AWS account details in deploy_to_aws.ps1
.\deploy_to_aws.ps1
```

### Option 2: Manual Deployment

```bash
# Create ECR repository
aws ecr create-repository --repository-name bike-share-lambda --region us-east-2

# Login to ECR
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-2.amazonaws.com

# Tag and push image
docker tag bike-share-lambda:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-2.amazonaws.com/bike-share-lambda:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-2.amazonaws.com/bike-share-lambda:latest

# Create Lambda function via AWS Console
# 1. Go to Lambda → Create function
# 2. Choose "Container image"
# 3. Select your ECR image
# 4. Set memory: 512MB, timeout: 30s
```

## 🧪 Testing

### Local Testing

```python
import requests
import json

test_data = {
    "body": json.dumps({
        "features": {
            "yr": 1,          # Year (0: 2011, 1: 2012)
            "mnth": 7,        # Month (1-12)
            "hr": 17,         # Hour (0-23)
            "holiday": 0,     # Holiday (0: No, 1: Yes)
            "weekday": 4,     # Day of week (0-6)
            "workingday": 1,  # Working day (0: No, 1: Yes)
            "temp": 0.65,     # Normalized temperature
            "atemp": 0.7,     # Normalized feeling temperature
            "hum": 0.5,       # Normalized humidity
            "windspeed": 0.1, # Normalized wind speed
            "season_2": 0,    # Spring (0: No, 1: Yes)
            "season_3": 1,    # Summer (0: No, 1: Yes)
            "season_4": 0,    # Fall (0: No, 1: Yes)
            "weathersit_2": 0, # Mist/Cloudy (0: No, 1: Yes)
            "weathersit_3": 1, # Light Snow/Rain (0: No, 1: Yes)
            "weathersit_4": 0  # Heavy Rain/Snow (0: No, 1: Yes)
        }
    })
}

response = requests.post(
    "http://localhost:9000/2015-03-31/functions/function/invocations",
    json=test_data
)
print("Prediction:", response.json())
```

### AWS Lambda Testing

```bash
aws lambda invoke \
  --function-name bike-share-predictor \
  --payload file://test-payload.json \
  response.json
```

## 📊 Model Details

- **Algorithm**: Random Forest Regressor
- **Training Data**: Historical bike sharing data with weather conditions
- **Features**: 16 input features (weather, time, seasonality)
- **Output**: Predicted number of bikes (continuous value)
- **Model Size**: 7.9MB
- **Performance**: Trained on scikit-learn 1.6.1

### Input Features

| Feature        | Type  | Description             | Range              |
| -------------- | ----- | ----------------------- | ------------------ |
| `yr`           | int   | Year indicator          | 0 (2011), 1 (2012) |
| `mnth`         | int   | Month                   | 1-12               |
| `hr`           | int   | Hour of day             | 0-23               |
| `holiday`      | int   | Holiday flag            | 0 (No), 1 (Yes)    |
| `weekday`      | int   | Day of week             | 0-6 (Sun-Sat)      |
| `workingday`   | int   | Working day             | 0 (No), 1 (Yes)    |
| `temp`         | float | Normalized temperature  | 0-1                |
| `atemp`        | float | Normalized feeling temp | 0-1                |
| `hum`          | float | Normalized humidity     | 0-1                |
| `windspeed`    | float | Normalized wind speed   | 0-1                |
| `season_2`     | int   | Spring season           | 0 (No), 1 (Yes)    |
| `season_3`     | int   | Summer season           | 0 (No), 1 (Yes)    |
| `season_4`     | int   | Fall season             | 0 (No), 1 (Yes)    |
| `weathersit_2` | int   | Misty/Cloudy            | 0 (No), 1 (Yes)    |
| `weathersit_3` | int   | Light Snow/Rain         | 0 (No), 1 (Yes)    |
| `weathersit_4` | int   | Heavy Rain/Snow         | 0 (No), 1 (Yes)    |

## 📈 Performance Metrics

- **Container Size**: 1.74GB
- **Cold Start Time**: ~2-3 seconds
- **Warm Response Time**: ~200ms
- **Memory Usage**: 512MB allocated
- **Timeout**: 30 seconds
- **Concurrent Executions**: Auto-scaling

## 🌐 API Gateway Integration

For REST API endpoints, see `api_gateway_example.py` for implementation details:

```
POST /predict - Make bike demand prediction
GET /health   - Health check endpoint
OPTIONS /*    - CORS preflight handling
```

## 🔒 Security

- ✅ No hardcoded credentials
- ✅ Environment variable configuration
- ✅ IAM role-based permissions
- ✅ CORS headers configured
- ✅ Input validation and sanitization
- ✅ Comprehensive error handling

## 🐛 Troubleshooting

### Common Issues

1. **Package Version Mismatch**

   - Ensure scikit-learn version matches model training (1.6.1)
   - Rebuild container if package conflicts occur

2. **Permission Errors**

   - Verify AWS CLI configuration
   - Check IAM permissions for ECR and Lambda

3. **Container Build Failures**

   - Use Python 3.11 (not 3.13) for better compatibility
   - Check Docker daemon is running

4. **Model Loading Errors**
   - Verify `random_forest_bike_model.pkl` is in project root
   - Check file permissions and size

## 📚 Dependencies

```
numpy==1.26.4
pandas==2.1.4
scikit-learn==1.6.1
joblib==1.4.2
boto3==1.35.0
python-dotenv==1.0.1
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with AWS Lambda Python runtime
- Uses scikit-learn for machine learning
- Containerized with Docker
- Deployed on AWS serverless infrastructure

## 📞 Support

For questions or issues:

- Open an issue on GitHub
- Check the troubleshooting section
- Review AWS Lambda logs for debugging

---

**Happy Predicting!** 🚴‍♂️📊
#   b i k e - s h a r e - d e m a n d - M L 
 
 
