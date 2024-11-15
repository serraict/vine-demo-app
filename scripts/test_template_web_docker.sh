#!/bin/bash
set -e  # Exit on error

cd test-output/test_app

echo "Testing web interface in Docker..."

# Build the Docker image
echo "Building Docker image..."
docker compose build --quiet

# Start the container
echo "Starting Docker container..."
docker compose up -d

# Give the container and web server time to start
echo "Waiting for web server to start..."
sleep 5

# Test if server is responding
if curl -s http://localhost:7901 > /dev/null; then
    echo "Web interface is running successfully in Docker!"
    SUCCESS=true
else
    echo "Failed to access web interface in Docker"
    echo "Docker logs:"
    docker compose logs
    SUCCESS=false
fi

# Stop the container
echo "Stopping Docker container..."
docker compose down

# Exit with appropriate status
if [ "$SUCCESS" = true ]; then
    echo "Web interface Docker test completed successfully!"
    exit 0
else
    exit 1
fi
