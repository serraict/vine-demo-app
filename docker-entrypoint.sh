#!/bin/bash

# Print app info
cliapp about
echo "Started vine-app container."

# Set up environment for cron
printenv > /etc/environment

# Start cron in background
cron

# Start the web app and redirect its output to a log file
python -m vineapp.__web__ 2>&1 | tee -a /var/log/webapp.log &

# Use tail to follow both log files
tail -f /var/log/cron.log /var/log/webapp.log
