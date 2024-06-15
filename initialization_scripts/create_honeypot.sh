#!/bin/bash

# Navigate to the script's directory
cd "$(dirname "$0")"

# Set variables
IMAGE_NAME="honeypot-app"
CONTAINER_NAME="honeypot-app"
CONFIG_PATH="../honeypot-app/config/routing_config.json"
LOGS_PATH="../honeypot-app/logs"
HONEYPOT_APP_DIR="../honeypot-app"

# Function to start the container
start_container() {
    # Check if the container is already running
    if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
        echo "Container $CONTAINER_NAME is already running. Stopping and removing it..."
        docker stop $CONTAINER_NAME
        docker rm $CONTAINER_NAME
    elif [ "$(docker ps -aq -f status=exited -f name=$CONTAINER_NAME)" ]; then
        echo "Container $CONTAINER_NAME exists but is stopped. Removing it..."
        docker rm $CONTAINER_NAME
    fi

    # Navigate to the honeypot-app directory
    pushd $HONEYPOT_APP_DIR

    # Build the Docker image
    echo "Building the Docker image..."
    docker build -t $IMAGE_NAME .

    # Extract the honeypot port from the config file
    if [[ -f $CONFIG_PATH ]]; then
        HONEYPOT_PORT=$(jq -r '.[].honeypot_port' $CONFIG_PATH)
        if [[ -z $HONEYPOT_PORT ]]; then
            echo "Error: Could not find honeypot_port in $CONFIG_PATH"
            popd
            exit 1
        fi
    else
        echo "Error: Config file not found at $CONFIG_PATH"
        popd
        exit 1
    fi

    # Run the Docker container with the dynamic port
    echo "Running the Docker container on port $HONEYPOT_PORT..."
    docker run -d -p ${HONEYPOT_PORT}:${HONEYPOT_PORT} -v $(pwd)/logs:/app/logs --name $CONTAINER_NAME $IMAGE_NAME

    if [[ $? -eq 0 ]]; then
        echo "Container started successfully and is running on port $HONEYPOT_PORT"
    else
        echo "Error: Failed to start the container"
        popd
        exit 1
    fi

    # Return to the previous directory
    popd
}

# Function to stop the container
stop_container() {
    echo "Stopping the Docker container..."
    docker stop $CONTAINER_NAME
    if [[ $? -eq 0 ]]; then
        echo "Container stopped successfully"
    else
        echo "Error: Failed to stop the container"
        exit 1
    fi

    echo "Removing the Docker container..."
    docker rm $CONTAINER_NAME
    if [[ $? -eq 0 ]]; then
        echo "Container removed successfully"
    else
        echo "Error: Failed to remove the container"
        exit 1
    fi
}

# Main script logic
case "$1" in
    start)
        start_container
        ;;
    stop)
        stop_container
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        exit 1
        ;;
esac
