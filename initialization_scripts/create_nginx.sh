#!/bin/bash

# Check if Nginx is installed
if ! command -v nginx &> /dev/null
then
    echo "Nginx is not installed. Installing..."
    sudo apt update
    sudo apt install -y nginx
else
    echo "Nginx is already installed."
fi

# Load configuration from config.json
CONFIG_FILE="routing_config.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Config file not found: $CONFIG_FILE"
    exit 1
fi

DOMAIN=$(jq -r 'keys[0]' "$CONFIG_FILE")
TARGET=$(jq -r --arg DOMAIN "$DOMAIN" '.[$DOMAIN].target' "$CONFIG_FILE")
PORT=$(jq -r --arg DOMAIN "$DOMAIN" '.[$DOMAIN].port' "$CONFIG_FILE")
HONEYPOT_PATH=$(jq -r --arg DOMAIN "$DOMAIN" '.[$DOMAIN].honeypot_path' "$CONFIG_FILE")
HONEYPOT_PORT=$(jq -r --arg DOMAIN "$DOMAIN" '.[$DOMAIN].honeypot_port' "$CONFIG_FILE")
HONEYPOT_IP=$(jq -r --arg DOMAIN "$DOMAIN" '.[$DOMAIN].honeypot_ips[0]' "$CONFIG_FILE")

# Generate nginx.conf dynamically
NGINX_CONF="/etc/nginx/sites-available/$DOMAIN"

sudo tee "$NGINX_CONF" > /dev/null <<EOL
server {
    listen 80;
    server_name $DOMAIN;

    location $HONEYPOT_PATH {
        proxy_pass http://$HONEYPOT_IP:$HONEYPOT_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 300;
    }

    location / {
        proxy_pass $TARGET:$PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 300;
    }
}
EOL

# Enable the new configuration
sudo ln -sf "$NGINX_CONF" /etc/nginx/sites-enabled/

# Test the configuration for syntax errors
sudo nginx -t

# Restart Nginx to apply changes
if sudo systemctl restart nginx; then
    echo "Nginx has been restarted successfully."
else
    echo "Failed to restart Nginx."
    exit 1
fi
