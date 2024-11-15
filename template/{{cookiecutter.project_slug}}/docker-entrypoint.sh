#!/bin/bash

# Print version info
cliapp version
echo "Started {{cookiecutter.project_name}} container."

echo "Starting web server..."
python -m {{cookiecutter.project_slug}}.__web__ 2>&1 | tee -a /var/log/webapp.log &
WEB_PID=$!

# Check if process is running
if ps -p $WEB_PID > /dev/null; then
    echo "Web server started with PID $WEB_PID"
else
    echo "Failed to start web server"
    exit 1
fi

# Keep container running and show logs
tail -f /var/log/webapp.log
