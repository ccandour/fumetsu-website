#!/bin/bash

# Path to the default.conf file
CONF_FILE="/etc/nginx/conf.d/default.conf"

# Function to restart Nginx
restart_nginx() {
    echo "Configuration file changed. Restarting Nginx..."
    nginx -s reload
}

# Monitor the default.conf file for changes
inotifywait -m -e modify "$CONF_FILE" | while read -r; do
    restart_nginx
done