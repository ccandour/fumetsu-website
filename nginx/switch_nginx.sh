#!/bin/bash

# Define paths
NGINX_CONF_DIR="/etc/nginx/conf.d"
HTTPS_CONF_PATH="/tmp/https.conf"
DEFAULT_CONF="default.conf"

# Function to switch to HTTPS configuration
switch_to_https() {
    echo "Switching to HTTPS configuration..."
    mv "$HTTPS_CONF_PATH" "$NGINX_CONF_DIR/$DEFAULT_CONF"
    echo "Switched to HTTPS configuration."
}

# Switch to HTTPS configuration
switch_to_https