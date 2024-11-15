#!/bin/bash

# Print version info
cliapp version
echo "Started {{cookiecutter.project_name}} container."

# Start the web app and redirect its output to both the log file and stdout
python -m {{cookiecutter.project_slug}}.__web__ 2>&1 | tee -a /var/log/webapp.log &

# Keep container running and show logs
tail -f /var/log/webapp.log
