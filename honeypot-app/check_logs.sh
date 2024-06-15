#!/bin/bash

ACCESS_LOG="/app/logs/access.log"
COMMAND_LOG="/app/logs/command.log"
CRON_LOG="/app/logs/cron_execution.log"

echo "Running check_logs.sh at $(date)" >> $CRON_LOG

if [[ -s $ACCESS_LOG ]]; then
    curl -X POST --data-urlencode "type=ACCESS&payload=$(tail -n 10 $ACCESS_LOG)" http://host.docker.internal:8000/internal/logs
    echo "Sent access log data at $(date)" >> $CRON_LOG
fi

if [[ -s $COMMAND_LOG ]]; then
    curl -X POST --data-urlencode "type=COMMAND&payload=$(tail -n 10 $COMMAND_LOG)" http://host.docker.internal:8000/internal/logs
    echo "Sent command log data at $(date)" >> $CRON_LOG
fi
