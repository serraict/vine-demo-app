#!/bin/bash
set -e  # Exit on error

cd test-output/test_app

echo "Testing web interface..."
# Activate virtual environment
source .venv/bin/activate

# Create a temporary file for the server output
LOGFILE=$(mktemp)
echo "Server logs will be written to: $LOGFILE"

# Start web server in background with proper module resolution
PYTHONPATH=src python -m test_app.__web__ > $LOGFILE 2>&1 &
WEB_PID=$!

# Give the server more time to start
echo "Waiting for server to start..."
sleep 5

# Test if server is responding
if curl -s http://localhost:8080 > /dev/null; then
    echo "Web interface is running successfully!"
    SUCCESS=true
else
    echo "Failed to start web interface"
    echo "Server output:"
    cat $LOGFILE
    SUCCESS=false
fi

# Stop the web server
if [ -n "$WEB_PID" ]; then
    echo "Stopping web server (PID: $WEB_PID)..."
    kill $WEB_PID 2>/dev/null || true
    wait $WEB_PID 2>/dev/null || true
fi

# Clean up only if successful
if [ "$SUCCESS" = true ]; then
    rm $LOGFILE
else
    echo "Log file preserved at: $LOGFILE"
fi

# Deactivate virtual environment
deactivate

# Exit with appropriate status
if [ "$SUCCESS" = true ]; then
    echo "Web interface test completed successfully!"
    exit 0
else
    exit 1
fi
