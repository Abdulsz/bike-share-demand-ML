FROM public.ecr.aws/lambda/python:3.11

# Copy requirements
COPY requirements.txt ./

# Install packages - match the versions used for model training
RUN pip3 install --upgrade pip && \
    pip3 install --target "${LAMBDA_TASK_ROOT}" \
    numpy==1.26.4 \
    joblib==1.4.2 \
    boto3==1.35.0 \
    python-dotenv==1.0.1 \
    pandas==2.1.4 \
    scikit-learn==1.6.1

# Copy application code and model
COPY bike-share.py ${LAMBDA_TASK_ROOT}/
COPY random_forest_bike_model.pkl ${LAMBDA_TASK_ROOT}/

# Set the CMD to your handler
CMD ["bike-share.lambda_handler"] 