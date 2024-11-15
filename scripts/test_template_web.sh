#!/bin/bash
set -e  # Exit on error

cd test-output/test_app

echo "Testing web interface..."
# Activate virtual environment
source .venv/bin/activate

# Create a temporary file for the server output
LOGFILE=$(mktemp)

# Start web server in background with proper module resolution
PYTHONPATH=src python -m test_app.__web__ > $LOGFILE 2>&1 &
WEB_PID=$!

# Give the server a moment to start
sleep 2

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
kill $WEB_PID 2>/dev/null || true

# Clean up
rm $LOGFILE

# Deactivate virtual environment
deactivate

# Exit with appropriate status
if [ "$SUCCESS" = true ]; then
    echo "Web interface test completed successfully!"
    exit 0
else
    exit 1
fi
