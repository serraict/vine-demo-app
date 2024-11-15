#!/bin/bash
set -e  # Exit on error

cd test-output/test_app

echo "Testing web interface..."
# Activate virtual environment
source .venv/bin/activate

# Start web server in background with proper module resolution
PYTHONPATH=src python -m test_app.__web__ &
WEB_PID=$!

# Give the server a moment to start
sleep 2

# Test if server is responding
if curl -s http://localhost:8080 > /dev/null; then
    echo "Web interface is running successfully!"
else
    echo "Failed to start web interface"
    kill $WEB_PID
    exit 1
fi

# Stop the web server
kill $WEB_PID

# Deactivate virtual environment
deactivate

echo "Web interface test completed successfully!"
