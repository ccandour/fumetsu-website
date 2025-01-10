# Build the Nginx server
FROM nginx

# Install inotify-tools
RUN apt-get update && apt-get install -y inotify-tools

# Copy the .conf files
COPY ./http.conf /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/nginx.conf

# Copy the monitoring script
COPY ./watch_conf.sh /watch_conf.sh

# Remove the log files in order to remove symlink between nginx logs & container log paths to ensure logs are available in default nginx log path
RUN rm -f /var/log/nginx/*

# Start nginx with the HTTP configuration
CMD ["nginx", "-g", "daemon off;"]