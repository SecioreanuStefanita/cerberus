#!/bin/bash
set -o monitor

echo "Running entrypoint script..." | tee -a /app/logs/command.log

# Ensure cron is not already running
if pgrep cron >/dev/null 2>&1; then
    echo "Cron is already running" | tee -a /app/logs/command.log
else
    echo "Starting cron service..." | tee -a /app/logs/command.log
    service cron start
    if [ $? -ne 0 ]; then
        echo "Failed to start cron service" | tee -a /app/logs/command.log
        exit 1
    fi
fi

# Log all commands to a file
exec > >(tee -a /app/logs/command.log) 2>&1

# Check if config file exists
CONFIG_PATH="/app/config/routing_config.json"
if [[ ! -f $CONFIG_PATH ]]; then
    echo "Config file not found at $CONFIG_PATH!" | tee -a /app/logs/command.log
    exit 1
fi

# Load the configuration
echo "Loading configuration from $CONFIG_PATH..." | tee -a /app/logs/command.log
HONEYPOT_PORT=$(jq -r '.[].honeypot_port' $CONFIG_PATH)
if [[ -z $HONEYPOT_PORT ]]; then
    echo "Error: Could not find honeypot_port in $CONFIG_PATH" | tee -a /app/logs/command.log
    exit 1
fi

echo "Configuration loaded: honeypot_port=$HONEYPOT_PORT" | tee -a /app/logs/command.log

# Start the Flask app
echo "Starting the Flask app on port $HONEYPOT_PORT..." | tee -a /app/logs/command.log
python /app/app.py &
FLASK_PID=$!

# Log the Flask PID
echo "Flask app started with PID $FLASK_PID" | tee -a /app/logs/command.log

# Wait for the Flask app to exit
wait $FLASK_PID

# Log Flask app exit status
FLASK_EXIT_STATUS=$?
echo "Flask app exited with status $FLASK_EXIT_STATUS" | tee -a /app/logs/command.log

# Run the original command
exec "$@"
