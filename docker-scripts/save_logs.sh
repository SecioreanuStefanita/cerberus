#!/bin/bash
CONTAINER_NAME=vuln-flask-app

docker cp $CONTAINER_NAME:/app/logs/access.log ./access.log
docker cp $CONTAINER_NAME:/app/logs/command.log ./command.log
