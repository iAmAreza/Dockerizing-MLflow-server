# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the training script
COPY train_model.py .

# Set up MLflow with SQLite as the backend store
ENV MLFLOW_TRACKING_URI=sqlite:///mlflow.db

# Create a startup script
RUN echo '#!/bin/bash\n\
mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri sqlite:///mlflow.db --default-artifact-root /mlflow_data &\n\
sleep 5\n\
python train_model.py\n\
wait' > /app/start.sh && chmod +x /app/start.sh

# Run the startup script
CMD ["/app/start.sh"]
