import os
import json
import joblib
import boto3
import tempfile
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to store the loaded model
model = None
model_loaded = False

def load_model_from_local():
    """Load model from local file system (container)"""
    model_path = "/var/task/random_forest_bike_model.pkl"
    
    if os.path.exists(model_path):
        logger.info("Loading model from local container path")
        return joblib.load(model_path)
    else:
        raise FileNotFoundError(f"Model file not found at {model_path}")

def load_model_from_s3():
    """Fallback: Load model from S3 if not found locally"""
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION")
    )

    bucket_name = "bikeshare-ml"  
    s3_key = "random_forest_bike_model.pkl"
    tmp_file_path = os.path.join(tempfile.gettempdir(), "random_forest_bike_model.pkl")

    if not os.path.exists(tmp_file_path):
        logger.info("Model not found locally. Downloading from S3...")
        s3_client.download_file(bucket_name, s3_key, tmp_file_path)
    else:
        logger.info("Using cached model from /tmp")

    return joblib.load(tmp_file_path)

def load_model():
    """Load model - try local first, then S3 as fallback"""
    global model, model_loaded
    if model_loaded and model is not None:
        return model
    
    try:
        # Try loading from local container first
        model = load_model_from_local()
        logger.info("Model loaded successfully from container")
    except FileNotFoundError:
        # Fallback to S3 if local file not found
        logger.info("Local model not found, trying S3...")
        model = load_model_from_s3()
        logger.info("Model loaded successfully from S3")
    
    model_loaded = True
    return model

def predict_bike_demand(features: Dict[str, Any]) -> Dict[str, Any]:
    """Make prediction using the loaded model"""
    global model
    if model is None:
        raise Exception("Model is not loaded")

    try:
        import pandas as pd
        input_df = pd.DataFrame([features])
        prediction = model.predict(input_df)[0]

        return {
            "prediction": float(prediction),
            "features": features
        }
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise

def lambda_handler(event, context):
    """AWS Lambda handler function"""
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))

        if "features" not in body:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'features' in request body"})
            }

        features = body["features"]

        # Load model (synchronously)
        load_model()

        # Make prediction
        result = predict_bike_demand(features)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(result)
        }

    except Exception as e:
        logger.error(f"Handler error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
    
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(".env") 