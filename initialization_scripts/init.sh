#!/bin/bash

# Navigate to the initialization_scripts directory
cd "$(dirname "$0")/initialization_scripts"

# Run create_config.py
echo "Running create_config.py..."
python create_config_json.py
if [ $? -ne 0 ]; then
    echo "create_config.py failed. Exiting..."
    exit 1
fi
echo "create_config.py completed successfully."

# Run create_nginx.sh
echo "Running create_nginx.sh..."
./create_nginx.sh
if [ $? -ne 0 ]; then
    echo "create_nginx.sh failed. Exiting..."
    exit 1
fi
echo "create_nginx.sh completed successfully."

# Run create_honeypot.sh
echo "Running create_honeypot.sh..."
./create_honeypot.sh start
if [ $? -ne 0 ]; then
    echo "create_honeypot.sh failed. Exiting..."
    exit 1
fi
echo "create_honeypot.sh completed successfully."

# Navigate to the request-checker-app directory
cd ../request-checker-app

# Start the FastAPI application
echo "Starting the FastAPI application..."
uvicorn main:app --host 0.0.0.0 --port 8000
if [ $? -ne 0 ]; then
    echo "Failed to start the FastAPI application. Exiting..."
    exit 1
fi
