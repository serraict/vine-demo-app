#!/bin/bash

# Print version info
cliapp version
echo "Started {{cookiecutter.project_name}} container."

# Keep container running
tail -f /dev/null
