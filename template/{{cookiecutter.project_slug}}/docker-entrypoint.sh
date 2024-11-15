#!/bin/bash
set -x  # Print commands as they are executed

# Print version info
cliapp version
echo "Started {{cookiecutter.project_name}} container."

echo "Starting web server..."
python -m {{cookiecutter.project_slug}}.__web__ 2>&1 | tee -a /var/log/webapp.log &

# Keep container running and show logs
tail -f /var/log/webapp.log
