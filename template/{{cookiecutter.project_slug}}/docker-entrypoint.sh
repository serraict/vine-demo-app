#!/bin/bash

# Print version info
cliapp version
echo "Started {{cookiecutter.project_name}} container."

# Start web server in background
echo "Starting web server..."
python -m {{cookiecutter.project_slug}}.__web__ >> /var/log/webapp.log 2>&1 &

# Keep container running
tail -f /var/log/webapp.log
